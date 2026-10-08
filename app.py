from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Room, Guest, Booking, ServiceRequest, Staff, HousekeepingTask, Feedback
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hotel-secret-key-super-secure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Helper function to calculate analytics
def get_analytics_metrics():
    total_rooms = Room.query.count()
    occupied_rooms = Room.query.filter_by(status='Occupied').count()
    available_rooms = Room.query.filter_by(status='Available').count()
    dirty_rooms = Room.query.filter_by(status='Dirty').count()
    maintenance_rooms = Room.query.filter_by(status='Maintenance').count()

    occupancy_rate = round((occupied_rooms / total_rooms * 100), 1) if total_rooms > 0 else 0

    # Total revenue from all bookings
    total_revenue = db.session.query(db.func.sum(Booking.total_amount)).scalar() or 0.0

    # Booking counts by status
    confirmed_count = Booking.query.filter_by(booking_status='Confirmed').count()
    checked_in_count = Booking.query.filter_by(booking_status='Checked-In').count()
    checked_out_count = Booking.query.filter_by(booking_status='Checked-Out').count()

    # Room type popularity
    room_types = db.session.query(Room.room_type, db.func.count(Booking.id))\
        .join(Booking, Room.id == Booking.room_id)\
        .group_by(Room.room_type).all()

    room_type_data = {r[0]: r[1] for r in room_types}

    # Average rating
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).scalar() or 5.0

    return {
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "available_rooms": available_rooms,
        "dirty_rooms": dirty_rooms,
        "maintenance_rooms": maintenance_rooms,
        "occupancy_rate": occupancy_rate,
        "total_revenue": round(total_revenue, 2),
        "booking_stats": {
            "Confirmed": confirmed_count,
            "Checked-In": checked_in_count,
            "Checked-Out": checked_out_count
        },
        "room_type_popularity": room_type_data,
        "avg_rating": round(avg_rating, 1)
    }

# Page Routes
@app.route('/')
def dashboard():
    analytics = get_analytics_metrics()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    pending_tasks = HousekeepingTask.query.filter(HousekeepingTask.status != 'Completed').all()
    recent_requests = ServiceRequest.query.order_by(ServiceRequest.requested_at.desc()).limit(5).all()
    return render_template('index.html', analytics=analytics, bookings=recent_bookings, tasks=pending_tasks, requests=recent_requests)

@app.route('/booking')
def booking_page():
    rooms = Room.query.all()
    guests = Guest.query.all()
    bookings = Booking.query.order_by(Booking.id.desc()).all()
    return render_template('booking.html', rooms=rooms, guests=guests, bookings=bookings)

@app.route('/analytics')
def analytics_page():
    analytics = get_analytics_metrics()
    service_requests = ServiceRequest.query.order_by(ServiceRequest.requested_at.desc()).all()
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    guests = Guest.query.order_by(Guest.loyalty_points.desc()).all()
    bookings = Booking.query.filter(Booking.booking_status.in_(['Checked-In', 'Confirmed'])).all()
    return render_template('analytics.html', analytics=analytics, requests=service_requests, feedbacks=feedbacks, guests=guests, bookings=bookings)

@app.route('/staff')
def staff_page():
    staff_members = Staff.query.all()
    rooms = Room.query.all()
    tasks = HousekeepingTask.query.order_by(HousekeepingTask.assigned_at.desc()).all()
    return render_template('staff.html', staff=staff_members, rooms=rooms, tasks=tasks)

# API / Form Action Endpoints
@app.route('/api/booking/create', methods=['POST'])
def create_booking():
    data = request.form
    
    # Check or create guest
    guest = Guest.query.filter_by(email=data['email']).first()
    if not guest:
        guest = Guest(
            full_name=data['full_name'],
            email=data['email'],
            phone=data['phone'],
            id_proof_type=data['id_proof_type'],
            id_proof_number=data['id_proof_number'],
            loyalty_points=50 # Initial signup reward
        )
        db.session.add(guest)
        db.session.commit()

    room = Room.query.get(int(data['room_id']))
    if not room or room.status != 'Available':
        return jsonify({"success": False, "message": "Room is not available for booking."}), 400

    # Calculate price based on nights
    check_in = datetime.strptime(data['check_in_date'], '%Y-%m-%d')
    check_out = datetime.strptime(data['check_out_date'], '%Y-%m-%d')
    nights = max((check_out - check_in).days, 1)
    total_amount = nights * room.price_per_night

    booking = Booking(
        guest_id=guest.id,
        room_id=room.id,
        check_in_date=data['check_in_date'],
        check_out_date=data['check_out_date'],
        total_amount=total_amount,
        booking_status="Confirmed"
    )

    # Award guest loyalty points
    guest.loyalty_points += int(total_amount // 10)

    db.session.add(booking)
    db.session.commit()
    return redirect(url_for('booking_page'))

@app.route('/api/booking/status/<int:booking_id>', methods=['POST'])
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    
    if new_status in ['Checked-In', 'Checked-Out', 'Cancelled']:
        booking.booking_status = new_status
        if new_status == 'Checked-In':
            booking.room.status = 'Occupied'
        elif new_status == 'Checked-Out':
            booking.room.status = 'Dirty'
            # Auto-create housekeeping clean task
            auto_task = HousekeepingTask(
                room_id=booking.room.id,
                task_type="Standard Clean",
                priority="High",
                status="Pending"
            )
            db.session.add(auto_task)
        elif new_status == 'Cancelled':
            booking.room.status = 'Available'
        
        db.session.commit()
    return redirect(url_for('booking_page'))

@app.route('/api/service-request/create', methods=['POST'])
def create_service_request():
    booking_id = request.form.get('booking_id')
    service_type = request.form.get('service_type')
    details = request.form.get('details')

    req = ServiceRequest(
        booking_id=booking_id,
        service_type=service_type,
        details=details,
        status="Pending"
    )
    db.session.add(req)
    db.session.commit()
    return redirect(url_for('analytics_page'))

@app.route('/api/service-request/status/<int:req_id>', methods=['POST'])
def update_service_request(req_id):
    req_item = ServiceRequest.query.get_or_404(req_id)
    req_item.status = request.form.get('status')
    db.session.commit()
    return redirect(url_for('analytics_page'))

@app.route('/api/feedback/create', methods=['POST'])
def create_feedback():
    guest_id = request.form.get('guest_id')
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')

    fb = Feedback(guest_id=guest_id, rating=rating, comment=comment)
    db.session.add(fb)
    db.session.commit()
    return redirect(url_for('analytics_page'))

@app.route('/api/staff/create', methods=['POST'])
def create_staff():
    staff = Staff(
        name=request.form.get('name'),
        role=request.form.get('role'),
        phone=request.form.get('phone'),
        shift=request.form.get('shift'),
        status="Active"
    )
    db.session.add(staff)
    db.session.commit()
    return redirect(url_for('staff_page'))

@app.route('/api/housekeeping/task/create', methods=['POST'])
def create_task():
    task = HousekeepingTask(
        room_id=request.form.get('room_id'),
        staff_id=request.form.get('staff_id') or None,
        task_type=request.form.get('task_type'),
        priority=request.form.get('priority'),
        status="Pending"
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('staff_page'))

@app.route('/api/housekeeping/task/status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    task = HousekeepingTask.query.get_or_404(task_id)
    new_status = request.form.get('status')
    task.status = new_status

    if new_status == 'Completed':
        # If room was dirty, set it back to Available
        if task.room.status == 'Dirty':
            task.room.status = 'Available'
    elif new_status == 'In Progress':
        if task.room.status == 'Dirty':
            task.room.status = 'In Cleaning'

    db.session.commit()
    return redirect(url_for('staff_page'))

@app.route('/api/room/status/<int:room_id>', methods=['POST'])
def update_room_status(room_id):
    room = Room.query.get_or_404(room_id)
    room.status = request.form.get('status')
    db.session.commit()
    return redirect(url_for('staff_page'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

