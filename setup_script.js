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
      });
      reader.readAsBinaryString(myFile);
  }
}