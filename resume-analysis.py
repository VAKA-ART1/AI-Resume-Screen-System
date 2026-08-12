@app.route("/resume-analysis")
def resume_analysis():

    if "resume_path" not in session:
        return redirect("/upload")

    filepath = session["resume_path"]

    text = extract_text(filepath)

    skills = extract_skills(text)

    score = calculate_score(skills)

    session["ats_score"] = score

    recommended_jobs = recommend_jobs(skills, jobs)

    return render_template(
        "resume_analysis.html",
        ats_score=score,
        skills=skills,
        jobs=recommended_jobs[:5]
    )