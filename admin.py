from flask import Blueprint, render_template, session, redirect, url_for
from database import get_db_connection


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# =========================================================
# ADMIN ACCESS CHECK
# =========================================================

def admin_required():

    user = session.get("user")

    if not user:
        return False

    if user.get("role") != "admin":
        return False

    return True


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@admin_bp.route("/dashboard")
def dashboard():

    if not admin_required():
        return redirect(url_for("login"))

    user = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # =========================
    # TOTAL USERS
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM users
    """)
    total_users = cursor.fetchone()["total"]

    # =========================
    # TOTAL CANDIDATES
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM users
        WHERE role = 'candidate'
    """)
    total_candidates = cursor.fetchone()["total"]

    # =========================
    # TOTAL RECRUITERS
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM users
        WHERE role = 'recruiter'
    """)
    total_recruiters = cursor.fetchone()["total"]

    # =========================
    # TOTAL JOBS
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM jobs
    """)
    total_jobs = cursor.fetchone()["total"]

    # =========================
    # TOTAL APPLICATIONS
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
    """)
    total_applications = cursor.fetchone()["total"]

    # =========================
    # SHORTLISTED APPLICATIONS
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE status = 'Shortlisted'
    """)
    shortlisted = cursor.fetchone()["total"]

    # =========================
    # RECENT USERS
    # =========================
    cursor.execute("""
        SELECT id, fullname, email, role, ats_score
        FROM users
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_users = cursor.fetchall()

    # =========================
    # RECENT JOBS
    # =========================
    cursor.execute("""
        SELECT *
        FROM jobs
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_jobs = cursor.fetchall()

    # =========================
    # RECENT APPLICATIONS
    # =========================
    cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY applied_at DESC
        LIMIT 5
    """)
    recent_applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",

        user=user,

        total_users=total_users,
        total_candidates=total_candidates,
        total_recruiters=total_recruiters,
        total_jobs=total_jobs,
        total_applications=total_applications,
        shortlisted=shortlisted,

        recent_users=recent_users,
        recent_jobs=recent_jobs,
        recent_applications=recent_applications
    )

# =========================================================
# MANAGE USERS
# =========================================================

@admin_bp.route("/users")
def users():

    if not admin_required():
        return redirect(url_for("login"))

    user = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            fullname,
            email,
            role,
            picture
        FROM users
        ORDER BY id DESC
        """
    )

    users = cursor.fetchall()

    cursor.close()
    conn.close()


    return render_template(
        "admin_users.html",
        user=user,
        users=users
    )


# =========================================================
# MANAGE JOBS
# =========================================================

@admin_bp.route("/jobs")
def jobs():

    if not admin_required():
        return redirect(url_for("login"))

    user = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            company,
            title,
            location,
            salary,
            experience,
            job_type,
            skills,
            description,
            responsibilities,
            qualifications,
            benefits
        FROM jobs
        ORDER BY id DESC
        """
    )

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()


    return render_template(
        "admin_jobs.html",
        user=user,
        jobs=jobs
    )


# =========================================================
# MANAGE APPLICATIONS
# =========================================================

@admin_bp.route("/applications")
def applications():

    if not admin_required():
        return redirect(url_for("login"))

    user = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            a.id,
            a.user_email,
            a.job_title,
            a.company,
            a.ats_score,
            a.status,
            a.applied_at,
            u.fullname
        FROM applications a
        LEFT JOIN users u
            ON a.user_email = u.email
        ORDER BY a.applied_at DESC
        """
    )

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_applications.html",
        user=user,
        applications=applications
    )

