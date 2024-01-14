function navigateToPrincipal() {
    window.location.href = "/principal";
}

function navigateToCounsellor() {
    window.location.href = "/counsellor";
}

function navigateToHOD() {
    window.location.href = "/HOD";
}

function navigateToStudent() {
    window.location.href = "/student";
}

function navigateToYearIncharge() {
    window.location.href = "/yearincharge";
}

function selectSingleDay() {
    var singleDayField = document.getElementById("singleDayForm");
    var multipleDaysField = document.getElementById("multipleDaysForm");
    singleDayField.style.display = "block";
    multipleDaysField.style.display = "none";
}

function selectMultipleDays() {
    var singleDayField = document.getElementById("singleDayForm");
    var multipleDaysField = document.getElementById("multipleDaysForm");
    singleDayField.style.display = "none";
    multipleDaysField.style.display = "block";
}

function validateFormOne() {
    var Date = document.getElementById("Date").value;

    if (!Date) {
        alert("Please select both start and end dates.");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}

function validateFormMultiple() {
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;

    if (!startDate || !endDate) {
        alert("Please select both start and end dates.");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}


