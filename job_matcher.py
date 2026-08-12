def recommend_jobs(user_skills, jobs):

    recommended = []

    for job in jobs:

        required = [skill.lower() for skill in job["skills"]]

        matched = 0

        for skill in user_skills:
            if skill.lower() in required:
                matched += 1

        score = int((matched / len(required)) * 100)

        job["match"] = score

        recommended.append(job)

    recommended.sort(
        key=lambda x: x["match"],
        reverse=True
    )

    return recommended