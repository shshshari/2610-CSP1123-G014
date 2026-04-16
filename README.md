## Login & Authentication Feature:
This branch contains the core authentication logic for the project.

### Key Functionality:
* **User Registration:** Securely adds new users to `database.db`.
* **Session Management:** Uses `flask-login` to keep users signed in across pages.
* **Role-Based Access:** Logic included to differentiate between **Regular Users** and **Managers** (using a specific access code).
* **Form Validation:** Checks for unique emails and matching passwords.

### Current Logic (app.py):
The backend currently handles:
1. `GET /login`: Renders the login form.
2. `POST /login`: Validates credentials against the SQLite database.
3. `POST /register`: Hashes passwords and saves new user profiles.
