from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False) # Deluxe, Suite, Standard, Penthouse
    price_per_night = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), default='Available') # Available, Occupied, Dirty, Maintenance
    image_url = db.Column(db.String(255), nullable=True)
    amenities = db.Column(db.String(255), nullable=True) # WiFi, Ocean View, Mini Bar, King Bed

    bookings = db.relationship('Booking', backref='room', lazy=True)
    housekeeping_tasks = db.relationship('HousekeepingTask', backref='room', lazy=True)

class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    id_proof_type = db.Column(db.String(50), nullable=False) # Passport, Driving License, National ID
    id_proof_number = db.Column(db.String(50), nullable=False)
    loyalty_points = db.Column(db.Integer, default=0)

    bookings = db.relationship('Booking', backref='guest', lazy=True)
    feedbacks = db.relationship('Feedback', backref='guest', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in_date = db.Column(db.String(20), nullable=False)
    check_out_date = db.Column(db.String(20), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    booking_status = db.Column(db.String(30), default='Confirmed') # Confirmed, Checked-In, Checked-Out, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service_requests = db.relationship('ServiceRequest', backref='booking', lazy=True)

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False) # Room Service, Housekeeping, Amenities, Maintenance
    details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='Pending') # Pending, In Progress, Completed
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False) # Front Desk, Housekeeping, Manager, Concierge, Maintenance
    phone = db.Column(db.String(20), nullable=False)
    shift = db.Column(db.String(30), default='Morning') # Morning, Evening, Night
    status = db.Column(db.String(30), default='Active') # Active, On Leave

    housekeeping_tasks = db.relationship('HousekeepingTask', backref='staff', lazy=True)

class HousekeepingTask(db.Model):
    __tablename__ = 'housekeeping_tasks'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    task_type = db.Column(db.String(50), nullable=False) # Deep Clean, Standard Clean, Turn-down, Maintenance
    priority = db.Column(db.String(20), default='Medium') # High, Medium, Low
    status = db.Column(db.String(30), default='Pending') # Pending, In Progress, Completed
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1 to 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
