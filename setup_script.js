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

function parseStudentData() {
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

function readConflicts() {
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
  console.log(team_size)
  if (team_size != ""){
    numTeams = calculateNumTeams(num_students, team_size);
    document.getElementById("insertNumTeams").innerHTML = numTeams;
  } else {
    document.getElementById("insertNumTeams").innerHTML = "";
  }
}

function calculateNumTeams(num_students, team_size) {
  return Math.floor(num_students / team_size) + Math.min(1, num_students % team_size);
}

function uploadStudentFile() {
  document.getElementById("nextstep").style.display = 'none';
  document.getElementById('student-buttonid').addEventListener('click', openDialog);
  function openDialog() {
      document.getElementById('student_data').click();
  }

  var input = document.getElementById('student_data' );
  var infoArea = document.getElementById( 'student-file-upload-filename' );

  input.addEventListener( 'change', showFileName )

  function showFileName( event ) {
    // the change event gives us the input it occurred in 
    var input = event.srcElement;

    // getting the name of the inputted file
    var fileName = input.files[0].name;

    // displaying the file name when a file is selected
    infoArea.textContent = 'File Name: ' + fileName;
    
    // error checking when a file is selected
    var splitFile = fileName.split("."); // Split the string using dot as separator
    var ext = splitFile.pop(); // Get last element 
    // getting the file
    const fi = document.getElementById('student_data'); 
    readConflicts(fi);
    if (ext != "csv") { // checking the file extention to make sure that it is a CSV
      document.getElementById("student-error").innerHTML = "Error: Incorrect file type. Ensure file type is CSV and click the Upload Student Data button to try again.";
      document.getElementById("nextstep").style.display = 'none';
      document.getElementById("student-successful").innerHTML = "";
    } else if (fi.files.length > 0) { 
        for (i = 0; i <= fi.files.length - 1; i++) { 
          const fsize = fi.files.item(i).size; 
          const file = Math.round((fsize / 1024)*1000000); // calculating the file size in bytes

          document.getElementById("student-error").innerHTML = "";
          document.getElementById("nextstep").style.display="inline-block";
          document.getElementById("student-successful").innerHTML = "Successful upload!";

          // The size of the file. 
          if (file >= 3000000) { // check for large files
              document.getElementById("student-error").innerHTML = "Error: File is too large. Please click the Upload Student Data button to try again.";
              document.getElementById("nextstep").style.display="none"; // hiding upload button
              document.getElementById("student-successful").innerHTML = "";
          } else if (file <= 0) { // check for empty files
              document.getElementById("student-error").innerHTML = "Error: File is empty. Please click the Upload Student Data button to try again.";
              document.getElementById("nextstep").style.display="none"; // hiding upload button
              document.getElementById("student-successful").innerHTML = "";
          }
      }
    }
  }
}



function uploadConflict() {
  document.getElementById("generate").style.display = 'none';
  document.getElementById('buttonid').addEventListener('click', openDialog);
  function openDialog() {
      document.getElementById('conflict_data').click();
  }

  var input = document.getElementById('conflict_data' );
  var infoArea = document.getElementById( 'file-upload-filename' );

  input.addEventListener( 'change', showFileName )

  function showFileName( event ) {
    // the change event gives us the input it occurred in 
    var input = event.srcElement;

    // getting the name of the inputted file
    var fileName = input.files[0].name;

    // displaying the file name when a file is selected
    infoArea.textContent = 'File Name: ' + fileName;
    
    // error checking when a file is selected
    var splitFile = fileName.split("."); // Split the string using dot as separator
    var ext = splitFile.pop(); // Get last element 
    // getting the file
    const fi = document.getElementById('conflict_data'); 
    readConflicts(fi);
    if (ext != "csv") { // checking the file extention to make sure that it is a CSV
      document.getElementById("error").innerHTML = "Error: Incorrect file type. Ensure file type is CSV and click the Upload Conflict File button to try again.";
      document.getElementById("generate").style.display = 'none';
      document.getElementById("successful").innerHTML = "";
    } else if (fi.files.length > 0) { 
        for (i = 0; i <= fi.files.length - 1; i++) { 
          const fsize = fi.files.item(i).size; 
          const file = Math.round((fsize / 1024)*1000000); // calculating the file size in bytes

          document.getElementById("error").innerHTML = "";
          document.getElementById("generate").style.display="inline-block";
          document.getElementById("successful").innerHTML = "Successful upload!";

          // The size of the file. 
          if (file >= 3000000) { // check for large files
              document.getElementById("error").innerHTML = "Error: File is too large. Please click the Upload Conflict File button to try again.";
              document.getElementById("generate").style.display="none"; // hiding upload button
              document.getElementById("successful").innerHTML = "";
          } else if (file <= 0) { // check for empty files
              document.getElementById("error").innerHTML = "Error: File is empty. Please click the Upload Conflict File button to try again.";
              document.getElementById("generate").style.display="none"; // hiding upload button
              document.getElementById("successful").innerHTML = "";
          }
      }
    }
  }
}

