from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Ticket, AdminUser, Feedback  # Import Ticket model
import qrcode
import os
import smtplib
import random
from email.mime.text import MIMEText


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'abcd1234'

# Initialize the database
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Configure SMTP settings
SMTP_SERVER = 'localhost'  # Change this to your local SMTP server
SMTP_PORT = 1025  # Change this if your SMTP server uses a different port

def send_email(recipient, subject, body):
    # Create a MIMEText object
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = 'your_email@example.com'  # Change this to your email address
    message['To'] = recipient

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.send_message(message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = AdminUser.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('admin_login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Generate random 6-digit OTP
        otp = ''.join(random.choices('0123456789', k=6))

        # Save email and OTP in session
        session['email'] = email
        session['username'] = username
        session['password'] = password
        session['otp'] = otp

        # Send email with OTP
        subject = 'OTP for Signup'
        body = f'Your OTP for signup is: {otp}'
        send_email(email, subject, body)

        # Redirect to OTP verification page
        return redirect(url_for('verify_otp'))

    return render_template('signup.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        # Get OTP entered by the user
        entered_otp = request.form['otp']

        # Get OTP from session
        stored_otp = session.get('otp')

        if entered_otp == stored_otp:
            # OTP verification successful
            username = session.get('username')
            password = session.get('password')
            email = session.get('email')

            # Create a new user object and add it to the database
            new_user = User(username=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully. You can now login.', 'success')
            session.pop('username')
            session.pop('password')
            session.pop('email')
            session.pop('otp')

            return redirect(url_for('login'))
        else:
            # OTP verification failed
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash('You need to login first', 'danger')
        return redirect(url_for('login'))
    # Fetch active tickets for the current user
    user = User.query.get(session['user_id'])
    
    # Check if the user object exists
    if user:
        tickets = user.tickets
        return render_template('user_dashboard.html', title='User Dashboard', tickets=tickets, user_username=user.username)
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        flash('You need to login first', 'danger')
        return redirect(url_for('admin_login'))
    user = AdminUser.query.get(session['user_id'])
    tickets = Ticket.query.all()
    feedbacks = Feedback.query.all()
    if user:
        return render_template('admin_dashboard.html', title='Admin Dashboard', tickets=tickets, user_username=user.username, feedbacks=feedbacks)
    return render_template('admin_dashboard.html')

@app.route('/book_ticket', methods=['GET', 'POST'])  
def book_ticket():
    if 'user_id' not in session:
        flash('You need to login first', 'danger')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':  
        start_point = request.form['start_point']
        stop_point = request.form['stop_point']
        
        # Store start and stop points in session
        session['start_point'] = start_point
        session['stop_point'] = stop_point
        print (session)
        flash('Ticket booked successfully', 'success')
        return redirect(url_for('pay'))  # Directly go to payment page after booking

    return render_template('book_ticket.html', user_username=user.username)

@app.route('/cancel_ticket/<int:ticket_id>', methods=['POST'])
def cancel_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        ticket.isActive = False
        db.session.commit()
        flash('Ticket canceled successfully', 'success')
    else:
        flash('Ticket not found', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/ticket/<int:ticket_id>')
def ticket_details(ticket_id):
    # Fetch the ticket from the database
    ticket = Ticket.query.get_or_404(ticket_id)
    user_id = session['user_id']
    
    # Generate a QR code for the ticket ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    ticket_string = str(ticket.id) + " " + str(ticket.start_point) + " " + str(ticket.stop_point)
    qr.add_data(ticket_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_path = 'images/' + str(user_id) + '-' + str(ticket.id) + '.png'
    img.save('static/' + img_path)  # Save the image temporarily
    
    return render_template('ticket_details.html', title='Ticket Details', ticket=ticket, img_path=img_path)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    return render_template("payment.html")

@app.route('/confirm_ticket', methods=['POST'])
def confirm_ticket():
    # Retrieve start and stop points from session
    start_point = session.get('start_point')
    stop_point = session.get('stop_point')
    
    # Check if start and stop points are available
    if start_point and stop_point:
        # Process the ticket confirmation
        # Clear the session variables for start and stop points if needed
        session.pop('start_point')
        session.pop('stop_point')
        ticket = Ticket(start_point=start_point, stop_point=stop_point, user_id=session['user_id'])
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket added successfully', 'success')
        return redirect(url_for('user_dashboard'))
    else:
        flash('Error: Start and stop points not found', 'danger')
        return redirect(url_for('book_ticket'))

@app.route('/ticket_scan')
def ticket_scan():
    return render_template('ticket_scan.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    email = request.form.get('email')
    message = request.form.get('message')

    if not email or not message:
        flash('Please provide both email and message', 'error')
        return redirect(url_for('contact_us'))

    feedback = Feedback(email=email, message=message)
    db.session.add(feedback)
    db.session.commit()

    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('contact_us'))

if __name__ == '__main__':
    app.run(debug=True)