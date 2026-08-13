# Vehicle Parking App

A Flask-based multi-user parking management app.

## Requirements

- Python 3.12+
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/wasimsal7/vehicle-parking-app.git
cd vehicle-parking-app
```

2. Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Install the required packages inside the virtual environment:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python run.py
```

5. Open your browser and visit:

```
http://127.0.0.1:5000
```

## Features

### Roles
- **Admin** — the superuser of the app, seeded automatically on first run (no registration required).
- **User** — registers and logs in to reserve parking spots.

### Admin
- Create, edit, and delete parking lots, including increasing or decreasing a lot's spot count.
- Spots are generated automatically based on a lot's maximum spot count — admin cannot add individual spots.
- Can only delete a lot once all its spots are empty.
- View the status of every parking spot, including vehicle details for occupied spots.
- View all registered users.
- View summary charts of parking lot/spot occupancy.

### User
- Register and log in.
- Choose an available parking lot — the app automatically allocates the first available spot; the user cannot pick a specific spot.
- Booking a spot marks it occupied immediately, with the parking-in timestamp recorded.
- Release the spot once done, recording the leaving timestamp and calculating cost.
- View a summary chart of time spent across past bookings.

## Default Admin Account

| Email | Password |
|-------|----------|
| admin@gmail.com | admin123 |

> Default database exists on download, otherwise a fresh SQLite database is created automatically on the first run.

## Project Structure

```
vehicle-parking-app/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   └── routes.py
├── instance/
├── static/
│   ├── images/
│   └── styles.css
├── templates/
│   ├── admin/
│   ├── user/
│   ├── error.html
│   ├── login.html
│   └── register.html
├── run.py
└── requirements.txt
```

## Technologies Used

- Flask
- Flask-SQLAlchemy
- SQLite
- Jinja2 (server-side templates)
- Matplotlib (for chart generation)
