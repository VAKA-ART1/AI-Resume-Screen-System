from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from database import get_db_connection
from ai_resume_parser import extract_text, extract_skills
from ats_score import calculate_score
from job_matcher import recommend_jobs
from jobs_data import jobs
from flask import send_from_directory
from recruiter import recruiter_bp
from admin import admin_bp

import os
# -----------------------------
# Flask App
# -----------------------------

app = Flask(__name__)

app.register_blueprint(admin_bp)

app.register_blueprint(recruiter_bp)

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY", "resume_screening_secret")

bcrypt = Bcrypt(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -----------------------------
# Google OAuth
# -----------------------------

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

# -----------------------------
# Home
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form.get("role", "candidate")

        # Only allow valid roles
        if role not in ["candidate", "recruiter"]:
            role = "candidate"

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check existing email
        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing = cursor.fetchone()

        if existing:

            flash("Email already exists!")

            cursor.close()
            conn.close()

            return redirect(url_for("register"))

        # Encrypt password
        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        # Resume
        resume_file = request.files.get("resume")
        resume_name = None

        if resume_file and resume_file.filename != "":

            filename = secure_filename(resume_file.filename)

            resume_file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            resume_name = filename

        # Insert user
        cursor.execute(
            """
            INSERT INTO users
            (
                fullname,
                email,
                password,
                role,
                resume,
                ats_score
            )
            VALUES(%s,%s,%s,%s,%s,%s)
            """,
            (
                fullname,
                email,
                hashed_password,
                role,
                resume_name,
                0
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Registration Successful!")

        return redirect(url_for("login"))

    return render_template("register.html")
# -----------------------------
# Email Login
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        print("LOGIN EMAIL:", email)
        print("PASSWORD RECEIVED:", bool(password))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        print("USER FOUND:", user is not None)

        if user:

            print("ROLE:", user["role"])

            try:
                password_correct = bcrypt.check_password_hash(
                    user["password"],
                    password
                )
            except Exception as e:
                print("PASSWORD ERROR:", e)
                password_correct = False

            print("PASSWORD CORRECT:", password_correct)

            if password_correct:

                session["user"] = {
                    "name": user["fullname"],
                    "email": user["email"],
                    "picture": user["picture"]
                    if user.get("picture")
                    else "https://ui-avatars.com/api/?name="
                         + user["fullname"],
                    "role": user["role"]
                }

                if user["role"] == "recruiter":
                    return redirect("/recruiter/dashboard")

                elif user["role"] == "admin":
                    return redirect("/admin/dashboard")

                else:
                    return redirect("/dashboard")

        flash("Invalid Email or Password")
        return redirect("/login")

    return render_template("login.html")

# -----------------------------
# Google Login
# -----------------------------

@app.route("/google-login")
def google_login():

    redirect_uri = url_for(
        "google_callback",
        _external=True
    )

    return google.authorize_redirect(redirect_uri)


# -----------------------------
# Google Callback
# -----------------------------
@app.route("/google/callback")
def google_callback():

    token = google.authorize_access_token()

    user = token["userinfo"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (user["email"],)
    )

    existing = cursor.fetchone()

    if existing is None:

        cursor.execute("""
        INSERT INTO users
        (fullname,email,google_id,picture)
        VALUES(%s,%s,%s,%s)
        """,
        (
            user["name"],
            user["email"],
            user["sub"],
            user["picture"]
        ))

        conn.commit()

    cursor.close()
    conn.close()

    session["user"] = {
        "name": user["name"],
        "email": user["email"],
        "picture": user["picture"]
    }

    return redirect("/dashboard")
# -----------------------------
# Logout
# -----------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
# -----------------------------
# Dashboard
# -----------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    email = session["user"]["email"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    # ================= USER =================

    cursor.execute(
        """
        SELECT id,
               fullname,
               email,
               phone,
               college,
               degree,
               cgpa,
               experience,
               resume,
               skills,
               ats_score,
               picture
        FROM users
        WHERE email=%s
        """,
        (email,)
    )

    user = cursor.fetchone()


    if not user:

        cursor.close()
        conn.close()

        return "User not found"


    # ================= APPLIED JOBS =================

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM applications
        WHERE user_email=%s
        """,
        (email,)
    )

    applied_result = cursor.fetchone()

    applied_jobs = (
        applied_result["total"]
        if applied_result
        else 0
    )


    # ================= SHORTLISTED =================

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM applications
        WHERE user_email=%s
        AND status='Shortlisted'
        """,
        (email,)
    )

    shortlisted_result = cursor.fetchone()

    shortlisted = (
        shortlisted_result["total"]
        if shortlisted_result
        else 0
    )


    # ================= AVAILABLE JOBS =================

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        """
    )

    jobs_result = cursor.fetchone()

    available_jobs = (
        jobs_result["total"]
        if jobs_result
        else 0
    )


    cursor.close()
    conn.close()


    return render_template(
        "dashboard.html",

        user=user,

        applied_jobs=applied_jobs,

        shortlisted=shortlisted,

        available_jobs=available_jobs,

        recent_activity=[]
    )


@app.route("/candidate")
def candidate():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get logged-in candidate details
    cursor.execute(
        """
        SELECT id, fullname, email, phone, college, degree,
               cgpa, experience, resume, skills, ats_score
        FROM users
        WHERE email=%s
        """,
        (session["user"]["email"],)
    )

    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return "User not found"

    # --------------------------------
    # GOOGLE PROFILE AVATAR
    # --------------------------------

    user["picture"] = session["user"].get("picture")

    # If fullname is empty, use Google name
    if not user.get("fullname"):
        user["fullname"] = session["user"].get(
            "name",
            user["email"]
        )

    # --------------------------------
    # Applied Jobs
    # --------------------------------

    cursor.execute(
        """
        SELECT company, job_title, status, applied_at
        FROM applications
        WHERE user_email=%s
        ORDER BY applied_at DESC
        """,
        (session["user"]["email"],)
    )

    applications = cursor.fetchall()

    # --------------------------------
    # Shortlisted Count
    # --------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) AS shortlisted
        FROM applications
        WHERE user_email=%s
        AND status='Shortlisted'
        """,
        (session["user"]["email"],)
    )

    shortlisted_result = cursor.fetchone()

    shortlisted = (
        shortlisted_result["shortlisted"]
        if shortlisted_result
        else 0
    )

    cursor.close()
    conn.close()

    # --------------------------------
    # ATS Score
    # --------------------------------

    ats_score = (
        user["ats_score"]
        if user["ats_score"] is not None
        else 0
    )

    return render_template(
        "candidate_dashboard.html",
        user=user,
        applications=applications,
        applied_jobs=len(applications),
        shortlisted=shortlisted,
        ats_score=ats_score
    )

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get current user
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (session["user"]["email"],)
    )
    user = cursor.fetchone()

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        college = request.form["college"]
        degree = request.form["degree"]
        cgpa = request.form["cgpa"]
        skills = request.form["skills"]
        experience = request.form["experience"]

        # Check if email already exists
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email=%s
            AND email!=%s
            """,
            (
                email,
                session["user"]["email"]
            )
        )

        existing = cursor.fetchone()

        if existing:
            flash("This email is already registered. Please login.")
            cursor.close()
            conn.close()
            return redirect("/edit-profile")

        resume = request.files.get("resume")

        print("Resume Object:", resume)

        if resume:
            print("Filename:", resume.filename)
        else:
            print("No resume received")

        resume_filename = user["resume"]
        ats_score = user["ats_score"] or 0

        # Upload Resume
        if resume and resume.filename != "":

            resume_filename = secure_filename(resume.filename)

            resume_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                resume_filename
            )

            resume.save(resume_path)

            print("Saved File:", resume_path)
            print("Filename:", resume_filename)

            try:

                text = extract_text(resume_path)

                print("Resume Text:")
                print(text)

                skills_list = extract_skills(text)

                print("Skills Found:", skills_list)

                ats_score = calculate_score(
                           skills_list,
                           text
                )

                print("ATS Score:", ats_score)

                skills = ", ".join(skills_list)

            except Exception as e:

                print("PDF Error:", e)

                flash("Invalid PDF. Please upload a valid PDF.")

                ats_score = 0

        # Update database
        cursor.execute(
            """
            UPDATE users
            SET
                fullname=%s,
                email=%s,
                phone=%s,
                college=%s,
                degree=%s,
                cgpa=%s,
                skills=%s,
                experience=%s,
                resume=%s,
                ats_score=%s
            WHERE email=%s
            """,
            (
                fullname,
                email,
                phone,
                college,
                degree,
                cgpa,
                skills,
                experience,
                resume_filename,
                ats_score,
                session["user"]["email"]
            )
        )

        conn.commit()

        session["user"]["name"] = fullname
        session["user"]["email"] = email

        flash("Profile Updated Successfully!")

        cursor.close()
        conn.close()

        return redirect("/candidate")

    cursor.close()
    conn.close()

    return render_template(
        "edit_profile.html",
        user=user
    )

@app.route("/calculate-ats", methods=["POST"])
def calculate_ats():

    if "user" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    resume = request.files.get("resume")

    if not resume or resume.filename == "":
        return jsonify({
            "success": False,
            "message": "Please select a resume"
        }), 400

    filename = secure_filename(resume.filename)

    # Only PDF
    if not filename.lower().endswith(".pdf"):
        return jsonify({
            "success": False,
            "message": "Please upload a PDF resume"
        }), 400

    resume_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    resume.save(resume_path)

    try:

        # Extract resume text
        text = extract_text(resume_path)

        if not text or not text.strip():
            return jsonify({
                "success": False,
                "message": "No readable text found in resume"
            }), 400

        # Extract skills
        skills_list = extract_skills(text)

        # Calculate ATS score
        ats_score = calculate_score(skills_list)

        # IMPORTANT:
        # Save ATS score in session
        session["ats_score"] = ats_score

        # Save resume, skills and ATS score into database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET resume=%s,
                skills=%s,
                ats_score=%s
            WHERE email=%s
            """,
            (
                filename,
                ", ".join(skills_list),
                ats_score,
                session["user"]["email"]
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "score": ats_score,
            "skills": skills_list
        })

    except Exception as e:

        print("ATS ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Unable to process this resume"
        }), 500

    
# -----------------------------
# Jobs Page
# -----------------------------
@app.route("/jobs")
def jobs():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    cursor.execute(
        """
        SELECT job_title
        FROM applications
        WHERE user_email=%s
        """,
        (session["user"]["email"],)
    )

    applied = cursor.fetchall()

    applied_jobs = [a["job_title"] for a in applied]

    for job in jobs:
        job["applied"] = job["title"] in applied_jobs

    cursor.close()
    conn.close()

    return render_template(
        "jobs.html",
        jobs=jobs
    )
#------------------------------
#jobs apply page
#-----------------------------
@app.route("/apply-job/<int:job_id>")
def apply_job(job_id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # --------------------------------------------------
    # 1. Get job details
    # --------------------------------------------------

    cursor.execute(
        "SELECT * FROM jobs WHERE id=%s",
        (job_id,)
    )

    job = cursor.fetchone()

    if not job:
        cursor.close()
        conn.close()
        return "Job not found"

    # --------------------------------------------------
    # 2. Get candidate ATS score from USERS table
    # --------------------------------------------------

    cursor.execute(
        """
        SELECT ats_score
        FROM users
        WHERE email=%s
        """,
        (session["user"]["email"],)
    )

    user_data = cursor.fetchone()

    if user_data and user_data["ats_score"] is not None:
        ats_score = user_data["ats_score"]
    else:
        ats_score = 0

    # --------------------------------------------------
    # 3. Check if candidate already applied
    # --------------------------------------------------

    cursor.execute(
        """
        SELECT *
        FROM applications
        WHERE user_email=%s
        AND job_title=%s
        """,
        (
            session["user"]["email"],
            job["title"]
        )
    )

    already = cursor.fetchone()

    # --------------------------------------------------
    # 4. Insert application
    # --------------------------------------------------

    if already is None:

        cursor.execute(
            """
            INSERT INTO applications
            (
                user_email,
                job_title,
                company,
                ats_score,
                status
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                session["user"]["email"],
                job["title"],
                job["company"],
                ats_score,
                "Applied"
            )
        )

        conn.commit()

    # --------------------------------------------------
    # 5. Close database
    # --------------------------------------------------

    cursor.close()
    conn.close()

    return redirect("/jobs")
# -----------------------------
# Upload Resume
# -----------------------------

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        flash("Please select a resume.")
        return redirect("/upload")

    file = request.files["resume"]

    if file.filename == "":
        flash("No file selected.")
        return redirect("/upload")

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    session["resume_path"] = filepath

    return redirect("/resume-analysis")


# -----------------------------
# Resume Analysis
# -----------------------------

@app.route("/resume-analysis")
def resume_analysis():

    if "resume_path" not in session:
        return redirect("/upload")

    return render_template(
        "resume_analysis.html",
        ats_score=0,
        skills=[],
        recommendations=[]
    )
@app.route("/recruiter")
def recruiter():

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        users.fullname,
        applications.*
    FROM applications
    JOIN users
    ON users.email = applications.user_email
    ORDER BY ats_score DESC
    """)

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "recruiter.html",
        applications=applications
    )

@app.route("/shortlist/<int:id>")
def shortlist(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET status='Shortlisted' WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/recruiter")


@app.route("/reject/<int:id>")
def reject(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET status='Rejected' WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/recruiter")

@app.route("/my-applications")
def my_applications():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM applications WHERE user_email=%s",
        (session["user"]["email"],)
    )

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "my_applications.html",
        applications=applications
    )

@app.route("/add-job", methods=["GET", "POST"])
def add_job():

    if request.method == "POST":

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO jobs
        (company,title,location,salary,experience,job_type,skills)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (

            request.form["company"],
            request.form["title"],
            request.form["location"],
            request.form["salary"],
            request.form["experience"],
            request.form["job_type"],
            request.form["skills"]

        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/jobs")

    return render_template("add_job.html")

@app.route("/job/<int:job_id>")
def job_details(job_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM jobs WHERE id=%s",
        (job_id,)
    )

    job = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "job_details.html",
        job=job
    )

@app.route("/ats-analysis")
def ats_analysis():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT fullname, email, skills, resume, ats_score
        FROM users
        WHERE email=%s
        """,
        (session["user"]["email"],)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return redirect("/login")

    skills = []

    if user["skills"]:
        skills = [
            skill.strip()
            for skill in user["skills"].split(",")
            if skill.strip()
        ]

    required_skills = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "flask",
        "mysql",
        "machine learning",
        "power bi"
    ]

    matched_skills = []
    missing_skills = []

    user_skills = [skill.lower() for skill in skills]

    for skill in required_skills:

        if skill.lower() in user_skills:
            matched_skills.append(skill.title())
        else:
            missing_skills.append(skill.title())

    score = user["ats_score"] or 0

    if score >= 80:
        status = "Good Resume"
        status_class = "success"
    elif score > 0:
        status = "Needs Improvement"
        status_class = "warning"
    else:
        status = "No Resume Uploaded"
        status_class = "secondary"

    return render_template(
        "ats_analysis.html",
        user=user,
        score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        status=status,
        status_class=status_class
    )

@app.route("/job-match/<int:job_id>")
def job_match(job_id):

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get current user
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (session["user"]["email"],)
    )

    user = cursor.fetchone()

    # Get selected job
    cursor.execute(
        "SELECT * FROM jobs WHERE id=%s",
        (job_id,)
    )

    job = cursor.fetchone()

    cursor.close()
    conn.close()

    if not job:
        return "Job not found", 404

    # Resume skills
    resume_skills = []

    if user and user["skills"]:
        resume_skills = [
            skill.strip().lower()
            for skill in user["skills"].split(",")
        ]

    # Job skills
    job_skills = []

    if job["skills"]:
        job_skills = [
            skill.strip().lower()
            for skill in job["skills"].split(",")
        ]

    # Find matching skills
    matched_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)

    # Find missing skills
    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    # Calculate job match percentage
    if len(job_skills) > 0:
        match_score = round(
            (len(matched_skills) / len(job_skills)) * 100
        )
    else:
        match_score = 0

    # Status
    if match_score >= 80:
        status = "Strong Match"
    elif match_score >= 50:
        status = "Moderate Match"
    else:
        status = "Weak Match"

    return render_template(
        "job_match.html",
        user=user,
        job=job,
        match_score=match_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        status=status
    )

@app.route("/recommended-jobs")
def recommended_jobs():

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get logged-in user
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (session["user"]["email"],)
    )

    user = cursor.fetchone()

    # Get all jobs
    cursor.execute("SELECT * FROM jobs")

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    # User resume skills
    resume_skills = []

    if user and user["skills"]:
        resume_skills = [
            skill.strip().lower()
            for skill in user["skills"].split(",")
            if skill.strip()
        ]

    recommended = []

    for job in jobs:

        job_skills = []

        if job["skills"]:
            job_skills = [
                skill.strip().lower()
                for skill in job["skills"].split(",")
                if skill.strip()
            ]

        # Calculate match
        if job_skills:

            matched_skills = [
                skill
                for skill in job_skills
                if skill in resume_skills
            ]

            match_score = round(
                (len(matched_skills) / len(job_skills)) * 100
            )

        else:

            matched_skills = []
            match_score = 0

        # Add only jobs with 50% or more match
        if match_score >= 50:

            job["match_score"] = match_score
            job["matched_skills"] = matched_skills

            if match_score >= 80:
                job["status"] = "Strong Match"
            else:
                job["status"] = "Moderate Match"

            recommended.append(job)

    # Highest match first
    recommended.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return render_template(
        "recommended_jobs.html",
        user=user,
        jobs=recommended
    )

@app.route("/recruiter/dashboard")
def recruiter_dashboard():

    # Check login
    if "user" not in session:
        return redirect("/login")

    # Only recruiter can access this page
    if session["user"].get("role") != "recruiter":
        flash("Access denied!")
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all available jobs
    cursor.execute("""
        SELECT *
        FROM jobs
        ORDER BY id DESC
    """)

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "recruiter_dashboard.html",
        user=session["user"],
        jobs=jobs
    )

if __name__ == "__main__":
    app.run(debug=True) 