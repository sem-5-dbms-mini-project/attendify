var analytics = JSON.parse(document.getElementById('analytics').textContent);

console.log("Hello");
var hello = "hello";

analyse = document.getElementById("analysisIframe");

const Absentees = document.createElement("iframe");

// Absentees.src = `${analytics['AbsenteesBar']}`;
Absentees.src = analytics['AbsenteesBar']
Absentees.height = "500"
Absentees.width = "500"

analyse.appendChild(Absentees);