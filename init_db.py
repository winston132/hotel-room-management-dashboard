from app import app
from models import db, Room, Guest, Booking, ServiceRequest, Staff, HousekeepingTask, Feedback
from datetime import datetime, timedelta

def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Seed Rooms
        rooms = [
            Room(room_number="101", room_type="Standard", price_per_night=120.0, capacity=2, status="Available", image_url="https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=500", amenities="WiFi, AC, TV, Queen Bed"),
            Room(room_number="102", room_type="Standard", price_per_night=120.0, capacity=2, status="Occupied", image_url="https://images.unsplash.com/photo-1590490360182-c33d57733427?w=500", amenities="WiFi, AC, TV, Twin Beds"),
            Room(room_number="201", room_type="Deluxe", price_per_night=220.0, capacity=2, status="Available", image_url="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=500", amenities="WiFi, AC, Balcony, King Bed, Mini Bar"),
            Room(room_number="202", room_type="Deluxe", price_per_night=230.0, capacity=3, status="Dirty", image_url="https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=500", amenities="WiFi, AC, City View, King Bed, Sofa"),
            Room(room_number="301", room_type="Suite", price_per_night=450.0, capacity=4, status="Occupied", image_url="https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500", amenities="WiFi, AC, Ocean View, Jacuzzi, Living Room, King Bed"),
            Room(room_number="302", room_type="Suite", price_per_night=480.0, capacity=4, status="Available", image_url="https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=500", amenities="WiFi, AC, Executive Lounge Access, King Bed, Dining Area"),
            Room(room_number="401", room_type="Penthouse", price_per_night=950.0, capacity=6, status="Maintenance", image_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500", amenities="WiFi, Private Pool, Butler Service, 3 Bedrooms, Panoramic View")
        ]
        db.session.add_all(rooms)
        db.session.commit()

        # Seed Guests
        guests = [
            Guest(full_name="Alice Vance", email="alice.vance@example.com", phone="+1-555-0192", id_proof_type="Passport", id_proof_number="P8942019", loyalty_points=350),
            Guest(full_name="Robert Chen", email="robert.chen@example.com", phone="+1-555-0143", id_proof_type="Driving License", id_proof_number="DL903184", loyalty_points=820),
            Guest(full_name="Sophia Martinez", email="sophia.m@example.com", phone="+1-555-0188", id_proof_type="National ID", id_proof_number="ID449102", loyalty_points=150),
            Guest(full_name="Marcus Brody", email="marcus.brody@example.com", phone="+1-555-0176", id_proof_type="Passport", id_proof_number="P7712390", loyalty_points=1200)
        ]
        db.session.add_all(guests)
        db.session.commit()

        # Seed Staff
        staff_members = [
            Staff(name="Elena Rostova", role="Front Desk", phone="+1-555-9011", shift="Morning", status="Active"),
            Staff(name="Carlos Mendez", role="Housekeeping", phone="+1-555-9022", shift="Morning", status="Active"),
            Staff(name="Sarah Jenkins", role="Housekeeping", phone="+1-555-9033", shift="Evening", status="Active"),
            Staff(name="David Miller", role="Maintenance", phone="+1-555-9044", shift="Morning", status="Active"),
            Staff(name="Liam Gallagher", role="Manager", phone="+1-555-9055", shift="Morning", status="Active")
        ]
        db.session.add_all(staff_members)
        db.session.commit()

        # Seed Bookings
        today = datetime.now().date()
        bookings = [
            Booking(guest_id=1, room_id=2, check_in_date=(today - timedelta(days=2)).isoformat(), check_out_date=(today + timedelta(days=2)).isoformat(), total_amount=480.0, booking_status="Checked-In"),
            Booking(guest_id=2, room_id=5, check_in_date=(today - timedelta(days=1)).isoformat(), check_out_date=(today + timedelta(days=3)).isoformat(), total_amount=1800.0, booking_status="Checked-In"),
            Booking(guest_id=3, room_id=3, check_in_date=(today + timedelta(days=5)).isoformat(), check_out_date=(today + timedelta(days=8)).isoformat(), total_amount=660.0, booking_status="Confirmed"),
            Booking(guest_id=4, room_id=4, check_in_date=(today - timedelta(days=5)).isoformat(), check_out_date=(today - timedelta(days=1)).isoformat(), total_amount=920.0, booking_status="Checked-Out")
        ]
        db.session.add_all(bookings)
        db.session.commit()

        # Seed Service Requests
        service_requests = [
            ServiceRequest(booking_id=1, service_type="Amenities", details="2 extra towels and hypoallergenic pillows", status="Completed"),
            ServiceRequest(booking_id=2, service_type="Room Service", details="Club Sandwich and Sparkling Water", status="In Progress"),
            ServiceRequest(booking_id=2, service_type="Housekeeping", details="Daily room cleaning requested at 2 PM", status="Pending")
        ]
        db.session.add_all(service_requests)

        # Seed Housekeeping Tasks
        housekeeping_tasks = [
            HousekeepingTask(room_id=4, staff_id=2, task_type="Deep Clean", priority="High", status="In Progress"),
            HousekeepingTask(room_id=2, staff_id=3, task_type="Standard Clean", priority="Medium", status="Pending"),
            HousekeepingTask(room_id=7, staff_id=4, task_type="Maintenance", priority="High", status="In Progress")
        ]
        db.session.add_all(housekeeping_tasks)

        # Seed Feedback
        feedbacks = [
            Feedback(guest_id=4, rating=5, comment="Exceptional service! The suite ocean view was breathtaking."),
            Feedback(guest_id=1, rating=4, comment="Very smooth check-in and friendly staff at front desk.")
        ]
        db.session.add_all(feedbacks)

        db.session.commit()
        print("Database initialized and successfully populated with seed data!")

if __name__ == "__main__":
    init_database()
