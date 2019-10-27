// Script file for HTML page: setup.html
var student_data;
var conflict_data;
var numStudents;

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

function generateTeams() {
  function convertArrayToJSON(array) {
    var new_array = "[";
    for (const row of array) {
      var new_row = "[";
      for (const cell of row) {
        new_row = new_row.concat('"', cell, '",');
      }
      new_row = new_row.slice(0, -1).concat("],");
      new_array = new_array.concat(new_row);
    }
    new_array = new_array.slice(0, -1).concat("]");
    console.log(new_array);
    return new_array;
  }

  event.preventDefault();

  sessionStorage.setItem('students', convertArrayToJSON(student_data))
  sessionStorage.setItem('conflicts', convertArrayToJSON(conflict_data))
  sessionStorage.setItem('team_size', document.getElementById("teamSize").value)

  window.location.href = "generate_teams.html";
  
}

function uploadStudentData() {
  let input = document.getElementById("student_data");
  if (input.files && input.files[0]) {
    var myFile = input.files[0];
    var reader = new FileReader();
    reader.addEventListener("load", function(e) {
      let csvdata = e.target.result;
      let parsedata = [];
      let newLinebrk = csvdata.split("\n");
      for (let i = 0; i < newLinebrk.length; i++) {
        parsedata.push(newLinebrk[i].split(","));
      }
      parsedata.splice(0, 1);
      student_data = parsedata;
    });
    reader.readAsBinaryString(myFile);
  }
}

function uploadConflicts() {
  let input = document.getElementById("conflict_data");
  if (input.files && input.files[0]) {
    var myFile = input.files[0];
    var reader = new FileReader();
    reader.addEventListener("load", function(e) {
      let csvdata = e.target.result;
      let parsedata = [];
      let newLinebrk = csvdata.split("\n");
      for (let i = 0; i < newLinebrk.length; i++) {
        parsedata.push(newLinebrk[i].split(","));
      }
      parsedata.splice(0, 1);
      conflict_data = parsedata;
    });
    reader.readAsBinaryString(myFile);
  }
}

function getNumStudents(array) {
  numStudents = array.length;
  document.getElementById("insertNumStudents").innerHTML = numStudents;
}

// Get number of teams, calculated from number of students and team size
function getNumTeams(num_students) {
  team_size = document.getElementById("teamSize").value;
  numTeams = calculateNumTeams(num_students, team_size);
  document.getElementById("insertNumTeams").innerHTML = numTeams;
}

function calculateNumTeams(num_students, team_size) {
  return Math.floor(num_students / team_size) + Math.min(1, num_students % team_size);
}
