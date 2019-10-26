// Script file for HTML page: setup.html
var finalParseData;
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

// Send data to Python model and go to teams page
function generateTeams() {
  event.preventDefault();
  window.location.href = "teams.html";
}

function upload() {
  let input = document.getElementById('student_data');
  if (input.files && input.files[0]) {
      console.log("FOUND FILE")
      var myFile = input.files[0];
      var reader = new FileReader();
      reader.addEventListener('load', function (e) {
          let csvdata = e.target.result;
          let parsedata = [];
          let newLinebrk = csvdata.split("\n");
          for(let i = 0; i < newLinebrk.length; i++) {
              parsedata.push(newLinebrk[i].split(","))
          }

          finalParseData = parsedata;
          console.log(finalParseData);

      });
      reader.readAsBinaryString(myFile);
  }

}

function getNumStudents(array){
  num = array.length - 1;
  numStudents = num;
  document.getElementById("insertNumStudents").innerHTML = numStudents;
  console.log(numStudents);
}

// Get number of teams, calculated from number of students and team size
function getNumTeams(num){
  teamSize = document.getElementById("teamSize").value;
  numTeams = num/teamSize;
  document.getElementById("insertNumTeams").innerHTML = numTeams;
}
