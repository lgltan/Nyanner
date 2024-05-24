# Nyanner
CSSECDEV Twitter but cats

# Requirements
Create a web application with the following features:
### 1) Registration screen
a) Full Name (either first-last or just full name)
b) Email (regex)
c) Phone number (accepts both +63 and 09)
d) Profile photo (check if valid photo)

### 2) Login screen

### 3) Administration panel - For admin users, it is ok to have a default admin account.

4) Security features discussed during class should be implemented (at least)
a) Anti brute-force protection
b) Password hashing with salting
c) Input validation (ie. email / phone number validate)
d) File upload type detection

### 5) Must be SQL-based

Due June 14 and prepare for a demo.
What needs to be uploaded via canvas is a SINGLE Zip file with the following
1) Source Code
2) Database schema 
3) Deployment instructions

# Libraries
### ReactJS
React Framework for frontend
### MySQL
Database for backend
### JWT
JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.
### bcrypt
Used for password hashing and salt
### redis
Used for anti-brute force as shown [here](https://stackoverflow.com/questions/19690950/preventing-brute-force-using-node-and-express-js)
### FileReader (vanilla JS)
Checking file type as shown [here](https://stackoverflow.com/questions/18299806/how-to-check-file-mime-type-with-javascript-before-upload)
### Email/Phone Number Verification (vanilla JS)
Checking Email/Phone Number Verification as shown [here](https://stackoverflow.com/questions/32776182/validation-for-email-or-phone-number-for-same-text-field-in-angularjs)