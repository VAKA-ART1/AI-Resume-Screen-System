from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from database import get_db_connection


# =========================================================
# RECRUITER BLUEPRINT
# =========================================================

recruiter_bp = Blueprint(
    "recruiter",
    __name__,
    url_prefix="/recruiter"
)


# =========================================================
# RECRUITER DASHBOARD
# =========================================================

@recruiter_bp.route("/dashboard")
def dashboard():

    # Check login
    if "user" not in session:
        return redirect("/login")

    # Only recruiter can access
    if session["user"].get("role") != "recruiter":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # Get all jobs
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

        # Number of jobs
        total_jobs = len(jobs)

        return render_template(
            "recruiter_dashboard.html",
            user=session["user"],
            jobs=jobs,
            total_jobs=total_jobs
        )

    finally:

        cursor.close()
        conn.close()


# =========================================================
# POST A JOB
# =========================================================

@recruiter_bp.route("/post-job", methods=["GET", "POST"])
def post_job():

    # Check login
    if "user" not in session:
        return redirect("/login")

    # Only recruiter
    if session["user"].get("role") != "recruiter":
        return redirect("/dashboard")

    # -----------------------------------------------------
    # GET REQUEST
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "post_job.html"
        )

    # -----------------------------------------------------
    # POST REQUEST
    # -----------------------------------------------------

    title = request.form.get("title", "").strip()
    company = request.form.get("company", "").strip()
    location = request.form.get("location", "").strip()
    salary = request.form.get("salary", "").strip()
    experience = request.form.get("experience", "").strip()
    job_type = request.form.get("job_type", "").strip()
    skills = request.form.get("skills", "").strip()
    description = request.form.get("description", "").strip()
    responsibilities = request.form.get(
        "responsibilities",
        ""
    ).strip()

    qualifications = request.form.get(
        "qualifications",
        ""
    ).strip()

    benefits = request.form.get(
        "benefits",
        ""
    ).strip()

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not title:
        flash("Job title is required!")
        return redirect("/recruiter/post-job")

    if not company:
        flash("Company name is required!")
        return redirect("/recruiter/post-job")

    if not location:
        flash("Location is required!")
        return redirect("/recruiter/post-job")

    if not skills:
        flash("Required skills are required!")
        return redirect("/recruiter/post-job")

    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO jobs
            (
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
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
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
            )
        )

        conn.commit()

        flash("Job Posted Successfully! 🚀")

        return redirect("/recruiter/dashboard")

    except Exception as e:

        conn.rollback()

        print("POST JOB ERROR:", e)

        flash(
            "Unable to post job. Please try again."
        )

        return redirect("/recruiter/post-job")

    finally:

        cursor.close()
        conn.close()


# =========================================================
# DELETE JOB
# =========================================================

@recruiter_bp.route("/delete-job/<int:job_id>", methods=["POST"])
def delete_job(job_id):

    # Check login
    if "user" not in session:
        return redirect("/login")

    # Only recruiter
    if session["user"].get("role") != "recruiter":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM jobs
            WHERE id=%s
            """,
            (job_id,)
        )

        conn.commit()

        flash("Job deleted successfully.")

    except Exception as e:

        conn.rollback()

        print("DELETE JOB ERROR:", e)

        flash("Unable to delete job.")

    finally:

        cursor.close()
        conn.close()

    return redirect("/recruiter/dashboard")


# =========================================================
# EDIT JOB
# =========================================================

@recruiter_bp.route(
    "/edit-job/<int:job_id>",
    methods=["GET", "POST"]
)
def edit_job(job_id):

    # Check login
    if "user" not in session:
        return redirect("/login")

    # Only recruiter
    if session["user"].get("role") != "recruiter":
        return redirect("/dashboard")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # Get job
        cursor.execute(
            """
            SELECT *
            FROM jobs
            WHERE id=%s
            """,
            (job_id,)
        )

        job = cursor.fetchone()

        if not job:

            flash("Job not found.")

            return redirect(
                "/recruiter/dashboard"
            )

        # -------------------------------------------------
        # GET
        # -------------------------------------------------

        if request.method == "GET":

            return render_template(
                "edit_job.html",
                job=job
            )

        # -------------------------------------------------
        # POST
        # -------------------------------------------------

        title = request.form.get(
            "title",
            ""
        ).strip()

        company = request.form.get(
            "company",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        salary = request.form.get(
            "salary",
            ""
        ).strip()

        experience = request.form.get(
            "experience",
            ""
        ).strip()

        job_type = request.form.get(
            "job_type",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        responsibilities = request.form.get(
            "responsibilities",
            ""
        ).strip()

        qualifications = request.form.get(
            "qualifications",
            ""
        ).strip()

        benefits = request.form.get(
            "benefits",
            ""
        ).strip()

        cursor.execute(
            """
            UPDATE jobs
            SET
                company=%s,
                title=%s,
                location=%s,
                salary=%s,
                experience=%s,
                job_type=%s,
                skills=%s,
                description=%s,
                responsibilities=%s,
                qualifications=%s,
                benefits=%s
            WHERE id=%s
            """,
            (
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
                benefits,
                job_id
            )
        )

        conn.commit()

        flash("Job updated successfully! ✅")

        return redirect(
            "/recruiter/dashboard"
        )

    except Exception as e:

        conn.rollback()

        print("EDIT JOB ERROR:", e)

        flash("Unable to update job.")

        return redirect(
            "/recruiter/dashboard"
        )

    finally:

        cursor.close()
        conn.close()

@recruiter_bp.route("/applicants/<int:job_id>")
def applicants(job_id):

    if "user" not in session:
        return redirect(url_for("login"))

    if session["user"]["role"] != "recruiter":
        return redirect(url_for("login"))

    recruiter_email = session["user"]["email"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check whether this job belongs to this recruiter
    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE id = %s
        AND recruiter_email = %s
    """, (job_id, recruiter_email))

    job = cursor.fetchone()

    if not job:
        cursor.close()
        conn.close()
        flash("Job not found or you don't have permission.")
        return redirect(url_for("recruiter.dashboard"))

    # Get applicants for this job
    cursor.execute("""
        SELECT
            a.id,
            a.user_email,
            a.job_title,
            a.company,
            a.ats_score,
            a.status,
            a.applied_at
        FROM applications a
        WHERE a.job_title = %s
        AND a.company = %s
        ORDER BY a.ats_score DESC, a.applied_at DESC
    """, (job["title"], job["company"]))

    applicants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "recruiter/applicants.html",
        user=session["user"],
        job=job,
        applicants=applicants
    )