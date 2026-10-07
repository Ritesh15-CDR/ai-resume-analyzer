const form = document.getElementById("resumeForm");
const fileInput = document.getElementById("resume");
const uploadText = document.querySelector(".upload-box span");


// Show selected file name
fileInput.addEventListener("change", function () {

    if (fileInput.files.length > 0) {
        uploadText.textContent =
            "📄 " + fileInput.files[0].name;
    } else {
        uploadText.textContent =
            "📄 Choose Resume PDF";
    }

});


// Analyze resume
form.addEventListener("submit", async function (event) {

    event.preventDefault();

    if (!fileInput.files.length) {
        alert("Please select a resume PDF.");
        return;
    }

    const formData = new FormData();

    formData.append(
        "resume",
        fileInput.files[0]
    );


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/analyze",
            {
                method: "POST",
                body: formData
            }
        );


        const result = await response.text();

        console.log("Backend Status:", response.status);
        console.log("Backend Result:", result);


        if (!response.ok) {
            throw new Error(result);
        }


        displayResults(result);


    } catch (error) {

        console.error("ERROR:", error);

        alert(
            "Something went wrong while analysing the resume.\n\n" +
            error.message
        );

    }

});



function displayResults(result) {

    document.getElementById("results").style.display = "block";


    // Resume Score
    const scoreMatch =
        result.match(/Resume Score:\s*(\d+)\/100/i);

    document.getElementById("resumeScore").textContent =
        scoreMatch
            ? scoreMatch[1] + "/100"
            : "--";


    // ATS Score
    const atsMatch =
        result.match(/ATS Score:\s*(\d+)\/100/i);

    document.getElementById("atsScore").textContent =
        atsMatch
            ? atsMatch[1] + "/100"
            : "--";


    // Skills Found
    const skillsMatch =
        result.match(
            /Skills Found:\s*([\s\S]*?)\s*ATS Score:/i
        );

    document.getElementById("skillsFound").textContent =
        skillsMatch
            ? skillsMatch[1].trim()
            : "No skills detected";


    // Missing Skills
    const missingMatch =
        result.match(
            /Missing \/ Recommended Skills:\s*([\s\S]*?)\s*Suggestions:/i
        );

    document.getElementById("missingSkills").textContent =
        missingMatch
            ? missingMatch[1].trim()
            : "No major missing skills";


    // Suggestions
    const suggestionMatch =
        result.match(
            /Suggestions:\s*([\s\S]*)/i
        );


    if (suggestionMatch) {

        const suggestions =
            suggestionMatch[1]
                .trim()
                .replace(/^- /gm, "• ");

        document.getElementById("suggestions").innerText =
            suggestions;

    } else {

        document.getElementById("suggestions").textContent =
            "No suggestions available.";

    }

}