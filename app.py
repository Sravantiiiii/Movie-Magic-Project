from flask import Flask, render_template, request, redirect, session, flash, url_for
import uuid
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ------------------------ Mock Databases ------------------------
mock_users = {}         # { email: hashed_password }
mock_bookings = []      # list of dicts for bookings

mock_movies = {
    "1": {
        "title": "Hidden Love",
        "image": "Hidden Love.png",
        "rating": "9.2/10",
        "duration": "3h 55m",
        "genre": "Dramatic",
        "price": 150
    },
    "2": {
        "title": "Subham",
        "image": "Subham.jpg",
        "rating": "10/10",
        "duration": "2h 40m",
        "genre": "Horror-Comedy",
        "price": 250
    },
    "3": {
        "title": "Kubera",
        "image": "Kubera.jpg",
        "rating": "10/10",
        "duration": "2h 30m",
        "genre": "Social Thriller",
        "price": 200
    }
}

# ------------------------ Routes ------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if email in mock_users:
            flash("Email already registered.")
            return redirect('/register')

        mock_users[email] = password
        flash("Registered successfully! Please log in.")
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if mock_users.get(email) == password:
            session['user'] = email
            flash("Login successful!")
            return redirect('/home')
        else:
            flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect('/login')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('home.html', user=session['user'], movies=mock_movies)

@app.route('/booking')
def booking_page():
    if 'user' not in session:
        return redirect('/login')
    movie = request.args.get('movie', 'Sample Movie')
    return render_template('booking_form.html', movie=movie)

def send_mock_email(email, movie, date, time, seat, booking_id):
    print(f"""EMAIL SENT TO: {email}
Booking Confirmed:
Movie: {movie}
Date: {date}
Time: {time}
Seat: {seat}
Booking ID: {booking_id}
""")

@app.route('/book', methods=['POST'])
def book_ticket():
    if 'user' not in session:
        return redirect('/login')

    booking = {
        'Email': session['user'],
        'Movie': request.form['movie'],
        'Date': request.form['date'],
        'Time': request.form['time'],
        'Seat': request.form['seat'],
        'BookingID': str(uuid.uuid4())
    }

    mock_bookings.append(booking)

    send_mock_email(
        booking['Email'],
        booking['Movie'],
        booking['Date'],
        booking['Time'],
        booking['Seat'],
        booking['BookingID']
    )

    flash("Booking successful!")
    return render_template('tickets.html', booking=booking)

@app.route('/tickets')
def tickets():
    if 'user' not in session:
        return redirect('/login')

    user_bookings = [b for b in mock_bookings if b['Email'] == session['user']]
    if not user_bookings:
        flash("No bookings found.")
        return redirect('/home')

    return render_template('tickets.html', booking=user_bookings[-1])

# ------------------------ Run App ------------------------

if __name__ == '__main__':
    app.run(debug=True)
