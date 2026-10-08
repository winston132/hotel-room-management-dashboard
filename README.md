# 🏨 Hotel Room Booking & Guest Experience Portal

An end-to-end web portal for hotel operations, guest booking registration, analytics dashboard, and housekeeping task lifecycle management built with **Python (Flask)**, **SQLite**, **Bootstrap 5**, and **Docker**.

---

## 🌟 Modules Breakdown

1. **Room Booking & Guest Registration**
   - Live room catalog & filtering by status and room type
   - Instant guest registration with ID proof verification
   - Interactive total cost estimation
   - Instant Check-In & Check-Out status workflow

2. **Booking Analytics & Guest Experience**
   - Real-time Chart.js analytics for revenue & room popularity
   - In-stay guest service request portal (room service, amenities, maintenance)
   - Guest feedback submission & ratings leaderboard
   - Loyalty points rewards program tracker

3. **Staff Management & Housekeeping Operations**
   - Live room cleanliness board (Clean, Dirty, In Cleaning, Out of Order)
   - Task assignment & priority dispatching for housekeeping staff
   - Staff directory roster with shift schedules

---

## 🚀 Running via Docker

### 1. Build the Docker Image
```bash
docker build -t hotel-booking-portal .
```

### 2. Run the Docker Container
```bash
docker run -d -p 5000:5000 --name hotel-app hotel-booking-portal
```

Open your web browser and navigate to: **`http://localhost:5000`**

---

## 📦 Running Locally (Without Docker)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database:**
   ```bash
   python init_db.py
   ```

3. **Run Application:**
   ```bash
   python app.py
   ```

---

## 🐙 Push Project to GitHub

```bash
# 1. Initialize Git Repository
git init

# 2. Stage All Project Files
git add .

# 3. Create Initial Commit
git commit -m "Initial commit - Hotel Room Booking & Guest Experience Portal"

# 4. Link your GitHub Repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# 5. Push to Main Branch
git branch -M main
git push -u origin main
```
