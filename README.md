# 🤖 AI Resume Screening & ATS

An **AI-powered Resume Screening and Applicant Tracking System (ATS)** designed to simplify the recruitment process by connecting **Candidates, AI Screening, Recruiters, and Administrators** in one intelligent platform.

The system helps candidates discover relevant opportunities while enabling recruiters to analyze resumes, evaluate ATS scores, match candidates with jobs, and identify suitable applicants more efficiently.

---

## 📌 Table of Contents

* [About the Project](#-about-the-project)
* [Problem Statement](#-problem-statement)
* [Objectives](#-objectives)
* [Key Features](#-key-features)
* [User Roles](#-user-roles)
* [System Workflow](#-system-workflow)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Website Sections](#-website-sections)
* [ATS Screening](#-ats-screening)
* [Job Matching](#-job-matching)
* [Installation](#-installation)
* [Running the Project](#-running-the-project)
* [Configuration](#-configuration)
* [GitHub Setup](#-github-setup)
* [Future Enhancements](#-future-enhancements)
* [Advantages](#-advantages)
* [Limitations](#-limitations)
* [Conclusion](#-conclusion)
* [Author](#-author)

---

## 🌟 About the Project

**AI Resume Screening & ATS** is a web-based recruitment platform developed to make the hiring process faster and more organized.

Traditional recruitment often requires recruiters to manually review a large number of resumes. This can be time-consuming and may make it difficult to consistently identify candidates whose skills and experience best match a particular job.

This project introduces an AI-assisted workflow where resumes can be uploaded, analyzed, scored, and matched with relevant job requirements.

The platform provides an interactive recruitment experience for:

* 👨‍💻 Candidates
* 🤖 AI Screening Engine
* 👔 Recruiters
* 🛡️ Administrators

---

## ❗ Problem Statement

Recruiters may receive hundreds or thousands of resumes for a single job opening.

Manual resume screening can result in:

* High recruitment time
* Large amounts of repetitive work
* Difficulty comparing candidates consistently
* Missed relevant skills
* Slow candidate selection
* Difficulty managing job applications
* Lack of centralized recruitment information

The proposed system addresses these challenges by providing an intelligent platform for resume screening, ATS scoring, and candidate-job matching.

---

## 🎯 Objectives

The main objectives of this project are:

1. Develop an AI-assisted resume screening platform.
2. Allow candidates to upload their resumes.
3. Extract and analyze relevant resume information.
4. Calculate an ATS-style matching score.
5. Match candidates with suitable job opportunities.
6. Help recruiters identify relevant candidates quickly.
7. Provide an organized recruitment workflow.
8. Provide administrators with platform management capabilities.
9. Create a modern, responsive, and interactive user interface.
10. Reduce the manual effort involved in initial resume screening.

---

# 🚀 Key Features

## 📄 Resume Upload

Candidates can upload their resumes through the platform.

The system can process the uploaded resume and use the extracted information for screening and matching.

---

## 🤖 AI Resume Screening

The system analyzes resume information and evaluates the candidate against job requirements.

The screening process can consider information such as:

* Skills
* Programming languages
* Technical knowledge
* Experience
* Job-related keywords
* Educational information
* Relevant technologies

---

## 📊 ATS Score

The platform provides an ATS-style matching score to indicate how closely a candidate's resume matches a job requirement.

Example:

```text
ATS Score: 95%

Match Status:
Excellent Match
```

Higher matching scores indicate stronger alignment with the selected job requirements.

---

## 🎯 Smart Job Matching

The platform can recommend relevant jobs based on candidate skills and resume information.

Example:

```text
Python Developer
AI Engineer
Machine Learning Engineer
Data Analyst
Software Engineer
Full Stack Developer
```

---

## 👔 Recruiter Dashboard

Recruiters can use the platform to:

* Review candidates
* Analyze resume information
* View ATS scores
* Compare applicants
* Identify suitable candidates
* Review job applications
* Select candidates

---

## 👨‍💻 Candidate Experience

Candidates can:

* Register
* Login
* Upload resumes
* View recommended jobs
* Explore job opportunities
* Track recruitment progress
* View relevant opportunities

---

## 🛡️ Admin Management

Administrators can manage the recruitment platform and maintain system-level information.

Possible administrative responsibilities include:

* User management
* Recruiter management
* Candidate management
* Job management
* Platform monitoring
* Recruitment data management

---

# 👥 User Roles

The system is designed around four major roles.

### 1. 👨‍💻 Candidate

Candidates can:

* Register
* Login
* Upload resume
* View jobs
* Receive job recommendations
* Apply for suitable positions

### 2. 🤖 AI Engine

The AI component is responsible for:

* Resume analysis
* Skill identification
* ATS-style scoring
* Candidate-job matching

### 3. 👔 Recruiter

Recruiters can:

* Post/manage jobs
* Review candidates
* Analyze resumes
* View matching scores
* Select suitable candidates

### 4. 🛡️ Admin

Administrators can:

* Manage users
* Manage recruiters
* Manage candidates
* Manage jobs
* Monitor the platform

---

# 🔄 System Workflow

The overall workflow is:

```text
Candidate
    │
    ▼
Register / Login
    │
    ▼
Upload Resume
    │
    ▼
Resume Processing
    │
    ▼
AI Resume Screening
    │
    ▼
Skill & Keyword Analysis
    │
    ▼
ATS Score Calculation
    │
    ▼
Job Matching
    │
    ▼
Recruiter Review
    │
    ▼
Candidate Selection
    │
    ▼
Recruitment Process
```

---

# 🧠 AI Screening Workflow

The AI screening process can be represented as:

```text
Resume
   ↓
Text Extraction
   ↓
Information Processing
   ↓
Skill Identification
   ↓
Job Requirement Comparison
   ↓
Match Score
   ↓
Candidate Ranking
```

---

# 🛠️ Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap
* Font Awesome

## Backend

* Python
* Flask

## Database

* SQLite / relational database configuration depending on the project setup

## AI / Machine Learning

Potential components include:

* Python
* Machine Learning
* Natural Language Processing
* Resume text processing
* Keyword matching
* Candidate-job matching

## Development Tools

* Visual Studio Code
* Git
* GitHub
* Python Virtual Environment

---

# 📂 Project Structure

A typical project structure is:

```text
AI-Resume-Screen-System/
│
├── app.py
│
├── models/
│   └── ...
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── ...
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── ...
│   │
│   └── images/
│       └── ...
│
├── uploads/
│   └── ...
│
├── requirements.txt
│
└── README.md
```

> The exact structure may change as additional features are added to the project.

---

# 🎨 Website Design

The homepage is designed as a modern AI recruitment platform.

It includes:

### Hero Section

The hero section introduces the platform with:

* AI recruitment messaging
* Resume screening visualization
* ATS score animation
* Candidate selection animation
* Recruiter-candidate interaction
* Animated background elements

### Live Platform Activity

The platform visually represents the workflow:

```text
Candidate
    ↓
AI Engine
    ↓
Recruiter
    ↓
Admin
```

### Job Matching Section

The homepage displays job opportunities with:

* Job title
* Company
* Location
* Salary range
* Matching information

The job cards can be animated to create a continuously moving recruitment/job-matching experience.

---

# 📊 ATS Screening

The ATS component is designed to provide an easy-to-understand candidate matching score.

For example:

```text
Candidate: Priya Sharma

Role:
Machine Learning Engineer

ATS Score:
95%

Result:
Excellent Match
```

Possible score interpretation:

| Score     | Match             |
| --------- | ----------------- |
| 90–100%   | Excellent Match   |
| 80–89%    | Strong Match      |
| 70–79%    | Good Match        |
| Below 70% | Needs Improvement |

> These ranges are illustrative and can be adjusted according to the actual scoring implementation.

---

# 💼 Job Matching

The job matching feature connects candidate profiles with relevant opportunities.

Example:

```text
Candidate Skills

Python
Machine Learning
SQL
Flask
Data Analysis
```

Possible recommended positions:

```text
Machine Learning Engineer
Python Developer
Data Scientist
AI Engineer
Data Analyst
```

This allows candidates to discover opportunities related to their skills.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/VAKA-ART1/AI-Resume-Screen-System.git
```

## 2. Navigate to the Project

```bash
cd AI-Resume-Screen-System
```

## 3. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
```

## 4. Activate the Virtual Environment

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If activation is blocked, PowerShell may require:

```powershell
Set-ExecutionPolicy -Scope Process RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

After installing dependencies, run the Flask application:

```bash
python app.py
```

Depending on the Flask configuration, the application will be available at:

```text
http://127.0.0.1:5000/
```

Open the URL in your browser.

---

# 🔐 Configuration

Before running the application, verify the following:

* Python is installed.
* Virtual environment is activated.
* Required packages are installed.
* Database configuration is correct.
* Upload directories exist.
* Environment variables are configured if required.
* Flask application settings are correct.

For production deployment, sensitive information such as:

* Secret keys
* Database passwords
* API keys
* Authentication credentials

should be stored securely using environment variables rather than directly inside source code.

---

# 🧪 Testing

The application should be tested for:

### Candidate

* Registration
* Login
* Resume upload
* Job browsing
* Job matching
* Application workflow

### Recruiter

* Login
* Job management
* Candidate viewing
* Resume screening
* ATS score viewing
* Candidate selection

### Admin

* Authentication
* User management
* Job management
* Platform management

### UI

* Desktop responsiveness
* Mobile responsiveness
* Navigation
* Animations
* Buttons
* Forms
* Resume upload interface

---

# 🔒 Security Considerations

The system should follow basic web security practices such as:

* Secure authentication
* Password hashing
* Input validation
* File type validation
* File size restrictions
* Secure file uploads
* Protection against unauthorized access
* Secure handling of user data
* Environment-based secret management

Resume files may contain sensitive personal information, so uploaded documents should be handled carefully.

---

# 📈 Advantages

The proposed system provides several advantages:

* ⚡ Faster initial resume screening
* 🤖 AI-assisted candidate evaluation
* 📊 ATS-style candidate scoring
* 🎯 Better job matching
* 👔 Reduced recruiter workload
* 📄 Centralized resume management
* 👥 Multi-role recruitment workflow
* 🌐 Web-based accessibility
* 🎨 Modern user interface
* 📱 Responsive design

---

# ⚠️ Limitations

The system may have limitations depending on the current implementation:

* ATS scoring depends on the implemented matching logic.
* Resume formats may affect text extraction.
* AI-generated scores should not be treated as the only basis for hiring decisions.
* Job recommendations depend on available job data.
* Real-world recruitment requires human review.
* Production deployment requires additional security and scalability measures.

---

# 🔮 Future Enhancements

Several features can be added in future versions.

## 🤖 Advanced AI

* NLP-based resume understanding
* Semantic skill matching
* AI candidate ranking
* Experience-level analysis
* Job description understanding

## 📄 Resume Features

* Automatic resume parsing
* Resume quality analysis
* Missing keyword detection
* Resume improvement suggestions
* Resume comparison

## 💼 Recruitment Features

* Interview scheduling
* Email notifications
* Candidate status tracking
* Recruiter communication
* Application tracking

## 📊 Analytics

* Recruitment analytics dashboard
* Candidate statistics
* Job performance analytics
* Hiring funnel visualization
* Recruiter performance analytics

## 🔐 Security

* OAuth authentication
* Two-factor authentication
* Role-based access control
* Secure cloud storage
* Audit logs

## ☁️ Deployment

Future versions can be deployed using cloud platforms such as:

* AWS
* Microsoft Azure
* Google Cloud
* Render
* Railway
* PythonAnywhere

---

# 🌐 GitHub Repository

Project repository:

**AI Resume Screening & ATS**

https://github.com/VAKA-ART1/AI-Resume-Screen-System

---

# 📌 Project Status

```text
Project Status: Active Development 🚀
```

The project is continuously being improved with new UI features, recruitment workflows, resume screening capabilities, and job matching functionality.

---

# 🎓 Academic Project

This project can be used as a **B.Tech Computer Science and Engineering project** demonstrating the integration of:

* Web Development
* Python
* Flask
* Artificial Intelligence
* Resume Processing
* Applicant Tracking
* Job Recommendation
* Database Management
* UI/UX Design

It demonstrates how AI-assisted technologies can be integrated into a practical recruitment workflow.

---

# 🏁 Conclusion

The **AI Resume Screening & ATS** project provides an intelligent and user-friendly approach to modern recruitment.

The system brings together **candidates, AI-based resume screening, recruiters, and administrators** into a unified platform. By analyzing resumes, generating ATS-style matching scores, and recommending relevant job opportunities, the platform aims to reduce the time and effort required for the initial stages of recruitment.

The project also demonstrates the practical application of **Python, Flask, web technologies, AI concepts, database management, and interactive UI design** in solving a real-world recruitment problem.

While AI can significantly improve the efficiency of candidate screening, the final hiring decision should remain under human supervision to ensure fairness, context-aware evaluation, and responsible recruitment.

Overall, this project provides a strong foundation for developing a **scalable, intelligent, and modern Applicant Tracking System** and can be further enhanced with advanced NLP, machine learning, analytics, cloud deployment, and secure authentication.

---

# 👨‍💻 Author

**Nagarani Vaka**

B.Tech — Computer Science and Engineering

### Technologies & Interests

* Python
* Java
* HTML
* CSS
* JavaScript
* Flask
* SQL
* Artificial Intelligence
* Machine Learning
* Data Analytics
* Web Development

---

## ⭐ If you find this project useful

Feel free to explore the repository, improve the project, and contribute new ideas.

**Built with Python, Flask, AI concepts, and modern web technologies. 🚀**
