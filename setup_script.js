// Script file for HTML page: setup.html
var finalParseData;
// Show/hide element based on div id and current state
function toggleVisiblity(tab) {
  var element = document.getElementById(tab);
  if (element.classList.contains("hidden")) {
    element.classList.remove("hidden");
  } else {
    element.classList.add("hidden");
  }
}

// Toggle visiblity of two different elements (tabs)
function nextTab(thisTab, nextTab) {
  toggleVisiblity(thisTab);
  toggleVisiblity(nextTab);
}

// Send data to Python model and go to teams page
function generateTeams() {
  event.preventDefault();
  window.location.href = "teams.html";
}

// Get number of students from the input file (read as an array)
function getNumStudents(array) {
  numStudents = array.length;
}

// Get number of teams, calculated from number of students and team size
function getNumTeams(numStudents, inputID){
  teamSize = document.getElementById(inputID).value;
  numTeams = (numStudents - 1)/teamSize
}
