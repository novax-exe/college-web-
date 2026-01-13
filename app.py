from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "CHANGE_ME_TO_A_RANDOM_SECRET_KEY"
app.permanent_session_lifetime = timedelta(minutes=60)

# ✅ Demo users (CHANGE these)
# Passwords are hashed for safety. Use /admin/create-user to add more.
USERS = {
    "admin": generate_password_hash("admin@123"),
    "student": generate_password_hash("student@123"),
}

COLLEGE_NAME = "THENI KAMMAVAR SANGAM COLLEGE OF TECHNOLOGY"


def is_logged_in():
    return "user" in session


@app.route("/")
def home():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("dashboard.html", college_name=COLLEGE_NAME, user=session.get("user"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # ✅ Confirm ID & Password required
        if not username or not password or not confirm_password:
            flash("User ID, Password and Confirm Password are required.", "danger")
            return redirect(url_for("login"))

        if password != confirm_password:
            flash("Password and Confirm Password do not match.", "danger")
            return redirect(url_for("login"))

        if username in USERS and check_password_hash(USERS[username], password):
            session.permanent = True
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid User ID or Password.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html", college_name=COLLEGE_NAME)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("profile.html", college_name=COLLEGE_NAME, user=session.get("user"))


@app.route("/about")
def about():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("about.html", college_name=COLLEGE_NAME)


@app.route("/admin/create-user", methods=["GET", "POST"])
def create_user():
    """
    Simple user creation page.
    In real projects, use a database.
    """
    if not is_logged_in() or session.get("user") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        new_user = request.form.get("new_user", "").strip()
        new_pass = request.form.get("new_pass", "")
        new_pass_confirm = request.form.get("new_pass_confirm", "")

        if not new_user or not new_pass or not new_pass_confirm:
            flash("All fields are required.", "danger")
            return redirect(url_for("create_user"))

        if new_pass != new_pass_confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("create_user"))

        if new_user in USERS:
            flash("User already exists.", "warning")
            return redirect(url_for("create_user"))

        USERS[new_user] = generate_password_hash(new_pass)
        flash(f"User '{new_user}' created successfully!", "success")
        return redirect(url_for("home"))

    return render_template("create_user.html", college_name=COLLEGE_NAME)


if __name__ == "__main__":
    app.run(debug=True)
