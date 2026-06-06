from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "sipms_secret_key"


def get_db():
    conn = sqlite3.connect("internship.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO students(name,email,phone,password)
                VALUES(?,?,?,?)
            """, (name, email, phone, password))

            conn.commit()

            flash("Registration Successful!", "success")
            return redirect("/login")

        except:
            flash("Email already exists!", "danger")

        conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM admins
            WHERE email=? AND password=?
        """, (email, password))

        admin = cur.fetchone()

        if admin:
            session["admin"] = email
            return redirect("/admin")

        cur.execute("""
            SELECT * FROM students
            WHERE email=? AND password=?
        """, (email, password))

        student = cur.fetchone()

        if student:
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]

            return redirect("/dashboard")

        flash("Invalid Credentials", "danger")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM applications
        WHERE student_id=?
    """, (session["student_id"],))

    applications = cur.fetchall()

    return render_template(
        "dashboard.html",
        applications=applications
    )


@app.route("/internships")
def internships():

    if "student_id" not in session:
        return redirect("/login")

    internships = [

        {
            "title": "Python Developer Intern",
            "company": "Infosys"
        },

        {
            "title": "Web Development Intern",
            "company": "TCS"
        },

        {
            "title": "Data Analyst Intern",
            "company": "Wipro"
        },

        {
            "title": "AI-ML Intern",
            "company": "Google"
        }

    ]

    return render_template(
        "internships.html",
        internships=internships
    )


@app.route("/apply/<path:title>/<company>")
def apply(title, company):

    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM applications
        WHERE student_id=?
        AND internship_title=?
    """, (session["student_id"], title))

    existing = cur.fetchone()

    if existing:

        flash("Already Applied!", "warning")

    else:

        cur.execute("""
            INSERT INTO applications
            (
            student_id,
            internship_title,
            company,
            status
            )
            VALUES(?,?,?,?)
        """,
                    (
                        session["student_id"],
                        title,
                        company,
                        "Applied"
                    ))

        conn.commit()

        flash("Application Submitted!", "success")

    conn.close()

    return redirect("/dashboard")


@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT applications.*,
               students.name
        FROM applications
        JOIN students
        ON applications.student_id=students.id
    """)

    applications = cur.fetchall()

    return render_template(
        "admin_dashboard.html",
        applications=applications
    )


@app.route("/update/<int:id>/<status>")
def update_status(id, status):

    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE applications
        SET status=?
        WHERE id=?
    """, (status, id))

    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)