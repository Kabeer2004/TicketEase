# TicketEase - A modern full-stack web application for ticket booking

TicketEase is a user-friendly ticket booking application that simplifies the process of booking tickets for various transportation services. With TicketEase, users can easily book tickets online, eliminating the need for physical tickets and long waiting times. This repository contains the source code for the TicketEase web application.

## Features

### 1. Effortless Ticket Booking
- Book tickets for transportation services online.
- Streamlined booking process for a hassle-free experience.

### 2. Paperless Ticketing
- Enjoy paperless ticketing with electronic tickets accessible on your mobile device.
- Reduce paper waste and contribute to environmental sustainability.

### 3. Instant Confirmation
- Receive immediate confirmation upon booking tickets.
- No more waiting for emails or calls to confirm your booking.

### 4. User-Friendly Interface
- Intuitive interface for easy navigation and seamless ticket booking.
- Minimal learning curve, suitable for users of all ages.

### 5. Secure Payment Processing
- Secure payment gateway for safe and reliable transactions.
- Multiple payment options available for user convenience.


## Tech Stack
This is my **first** full-stack application! The tech stack is a little weird but it does the job - certain components can be easily swapped out and replaced with more "industry standard" alternatives but for now, this is good enough.

The following tech stack was used for the creation of this web app:

### 1. Flask
Flask powers all the backend functionality for this webapp - it handles routing and all conditionally loaded data on various webpages. It also handles addition/deletion of data from the database as well as handling API routes.

### 2. TailwindCSS
I decided to go with TailwindCSS for the creation of this project because of all the freely available pre-made components that you can find online. That way, I could ensure a responsive and modern user experience without having to do too much work.

### 3. SQLite (running on SQLAlchemy in Python)
I used SQLAlchemy in Python for the creation of the database models that are saved as an SQLite DB in the /instances folder. The database handles everything related to signup and login and also handles saving of tickets and user feedback.

### 4. AIOSMTPD and SMTPLIB
I used these libraries for running a local SMTP mail server for sending and receiving emails. I wanted this project to be ready out of the box if anyone wished to download and use it, so I only added testing email functionality with this local server. Emails are used only for OTP verification as of now but can be easily expanded to do much more on the application such as sending mails on successful bookings, payment receipts and so on. 
The email sending logic in the app can easily be swapped out for something like Gmail or any other alternatives.

### The "industry standard" alternatives I was talking about
The backend could be swapped out for something like NextJS which offers SSR and other functionalities. If you wanted to continue with Python, you could switch to something like Django.
The database can be swapped out for any of the industry standard options - my personal choice would be MongoDB for its ease of use and popularity.


## Screenshots
### The Home Page
![ss4](https://github.com/Kabeer2004/TicketEase/assets/59280736/ad71b0d8-54df-4772-89d0-23f07d1f2a57)

### The Sign In page - very simple for now - external Authentication providers can be added here for authentication with Google or other accounts.
![ss5](https://github.com/Kabeer2004/TicketEase/assets/59280736/207c8ee9-e981-4c47-a284-2af6136bbac9)

### The User Dashboard allows you to see your current and past tickets and cancel any active tickets. 
![ss6](https://github.com/Kabeer2004/TicketEase/assets/59280736/2a4c34bc-f9ad-4bbc-b33e-68ce2d0ae7f0)

### The Stop Selection page is pretty simple for now and only includes stops from one route - this page can be expanded to include more routes and even calculate the cost of the ride depending on the stops selected by the user.
![ss7](https://github.com/Kabeer2004/TicketEase/assets/59280736/73d13e4b-3104-4885-baff-a990233487d0)

### Passengers can see their eTickets using the User Dashboard. The QR code can be used for ticket validation and cancellation when they board the bus.
![ss8](https://github.com/Kabeer2004/TicketEase/assets/59280736/ef08dbc7-2dbf-4e99-a59f-d92161e8603f)

### A view of the Admin Dashboard
![ss1](https://github.com/Kabeer2004/TicketEase/assets/59280736/446667ed-d99a-46ce-b7ef-fde6bda5bde2)

### The Admin Dashboard allows you to see booked tickets and user feedback.
![ss9](https://github.com/Kabeer2004/TicketEase/assets/59280736/8be232f5-f5b8-4442-8a19-6e0b2580e7f6)

### Ticket Scanning on the Admin Dashboard - this QR scanner can allow conductors on a bus to scan the QR code on a ticket and validate it. Once scanned, a ticket is automatically cancelled.
![ss2](https://github.com/Kabeer2004/TicketEase/assets/59280736/2df2a78f-f4e7-4761-a8d0-44cffc33ef16)


## Getting Started

To get started with TicketEase, follow these steps:

## Instructions to Run

### 1. Install Python
Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/).

### 2. Install Required Modules
Use pip to install the required Python modules:

```bash
python -m pip install flask sqlalchemy flask-mail flask-sqlalchemy aiosmtpd qrcode
```

### 3. Initialize the Database
(Optional) Run `dbinitialize.py` to initialize the database. You can skip this step if `site.db` already exists in the instance folder.

```bash
python dbinitialize.py
```

### 4. Run the Mail Server
Start the local SMTP server, which is used for sending emails to users.

```bash
python mailserver.py
```

### 5. Run the Main App
Run `app.py` to start the main application.

```bash
python app.py
```

### 6. Access the App
The app will be launched on `localhost`.



## Site Usage Instructions

### User Account Creation
1. Sign up to create a user account.
2. During signup, an OTP will be sent to the user's email address.
   - Note: Since real email sending logic is not set up, the email will be displayed in the terminal window where the mail server is running.
3. Verify the OTP from the terminal output.

### Ticket Booking
1. After verifying the OTP, you can proceed to book a ticket.
2. Once booked, you can view your ticket details.

### Admin Dashboard Access
1. Scroll down to the bottom of the homepage to find the admin login button.
2. Click on the admin login button to access the admin dashboard.

### Admin Dashboard Features
1. View current tickets and user feedback.
2. Cancel tickets from the table view.
3. Enter scanning mode to scan a ticket.
   
#### Admin Credentials
- Email: adminuser@ticketease.com
- Password: admin@ticketease

### Scanning Tickets
1. Hold up the QR code of the ticket in front of your camera.
2. Click the scan button.
3. The ticket will be scanned, validated, and then cancelled.



## Instructions for Editing the App

### Basic Editing
- Most changes can be made without installing anything additional.

### Editing/Addition of Tailwind CSS Classes
1. **Install npm (Node.js):** If you haven't already, install npm (Node.js) on your system.
   
2. **Install Tailwind CSS:** Run the following command in your terminal to install Tailwind CSS:
   ```
   npm install tailwindcss
   ```

3. **Run Tailwind CSS:** Execute the following command to compile Tailwind CSS and watch for changes:
   ```
   npx tailwindcss -i ./static/css/input.css -o ./static/dist/css/output.css --watch
   ```


## Contributing

Contributions to TicketEase are welcome! If you find any bugs or have suggestions for improvement, feel free to open an issue or submit a pull request.
