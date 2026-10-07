from flask import Flask, request, send_from_directory
from flask_cors import CORS
from pypdf import PdfReader
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(BASE_DIR, "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(BASE_DIR, "script.js")


@app.route("/analyze", methods=["POST"])
def analyze_resume():

    try:

        # Check resume upload
        if "resume" not in request.files:
            return "No resume uploaded", 400

        file = request.files["resume"]

        if file.filename == "":
            return "No file selected", 400

        # Read PDF
        reader = PdfReader(file)

        resume_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text + "\n"

        text_lower = resume_text.lower()


        # ==========================================
        # CAREER FIELD SKILLS
        # ==========================================

        skill_categories = {

            "IT / Software": [
                "python",
                "java",
                "javascript",
                "html",
                "css",
                "sql",
                "react",
                "angular",
                "node.js",
                "flask",
                "django",
                "php",
                "c",
                "c++",
                "git",
                "github"
            ],

            "Data / Analytics": [
                "excel",
                "advanced excel",
                "power bi",
                "tableau",
                "data analysis",
                "data visualization",
                "statistics",
                "data analytics",
                "sql"
            ],

            "Finance / Accounting": [
                "tally",
                "gst",
                "accounting",
                "financial analysis",
                "bookkeeping",
                "taxation",
                "ms excel",
                "excel"
            ],

            "Marketing": [
                "digital marketing",
                "seo",
                "sem",
                "google ads",
                "social media marketing",
                "content marketing",
                "email marketing",
                "branding",
                "market research"
            ],

            "HR": [
                "recruitment",
                "talent acquisition",
                "payroll",
                "hr management",
                "hrms",
                "employee relations",
                "human resources"
            ],

            "Sales / Business": [
                "sales",
                "crm",
                "lead generation",
                "business development",
                "negotiation",
                "customer service",
                "client management"
            ],

            "Design": [
                "figma",
                "canva",
                "photoshop",
                "illustrator",
                "ui/ux",
                "ui design",
                "ux design",
                "graphic design"
            ],

            "General / Professional": [
                "communication",
                "leadership",
                "teamwork",
                "problem solving",
                "time management",
                "project management",
                "ms word",
                "powerpoint"
            ]
        }


        # ==========================================
        # DETECT CAREER FIELD
        # ==========================================

        field_scores = {}

        for field, skills_list in skill_categories.items():

            count = 0

            for skill in skills_list:

                if skill in text_lower:
                    count += 1

            field_scores[field] = count


        detected_field = max(
            field_scores,
            key=field_scores.get
        )


        # If no field detected
        if field_scores[detected_field] == 0:
            detected_field = "General / Professional"


        # ==========================================
        # FIND SKILLS
        # ==========================================

        field_skills = skill_categories[detected_field]

        found_skills = []
        missing_skills = []


        for skill in field_skills:

            if skill in text_lower:
                found_skills.append(skill)

            else:
                missing_skills.append(skill)


        # ==========================================
        # RESUME SCORE
        # ==========================================

        score = 0

        score += min(
            len(found_skills) * 10,
            50
        )


        # ==========================================
        # RESUME SECTIONS
        # ==========================================

        suggestions = []

        sections = [
            "education",
            "experience",
            "skills",
            "projects",
            "contact"
        ]


        for section in sections:

            if section in text_lower:

                score += 10

            else:

                suggestions.append(
                    f"Consider adding a {section} section."
                )


        score = min(score, 100)


        # ==========================================
        # ATS SCORE
        # ==========================================

        ats_score = min(
            score + len(found_skills) * 5,
            100
        )


        # ==========================================
        # DEFAULT SUGGESTION
        # ==========================================

        if not suggestions:

            suggestions.append(
                "Your resume is well structured. "
                "Add measurable achievements and "
                "relevant skills to improve it further."
            )


        # ==========================================
        # FINAL RESULT
        # ==========================================

        result = f"""
RESUME ANALYSIS

Resume Score: {score}/100

Detected Career Field:
{detected_field}

Skills Found:
{", ".join(found_skills) if found_skills else "No relevant skills detected"}

ATS Score:
{ats_score}/100

Missing / Recommended Skills:
{", ".join(missing_skills[:5]) if missing_skills else "No major missing skills detected"}

Suggestions:
"""


        for suggestion in suggestions:

            result += f"- {suggestion}\n"


        return result


    except Exception as e:

        print("ERROR:", e)

        return (
            f"Resume analysis failed: {str(e)}",
            500
        )


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)