// Script file for HTML page: view_group.html
var dataStr;
var data;
var clickedID;
var teamNum;

// $.getJSON("data/output.json", function (json) {
//   sessionStorage.setItem("data", JSON.stringify(json));
//   getContent();
// });

// Get the size of an object
Object.size = function (obj) {
  var size = 0, key;
  for (key in obj) {
    if (obj.hasOwnProperty(key)) size++;
  }
  return size;
};

window.onload = function () {
  data = JSON.parse(sessionStorage.getItem('output'));
  this.sessionStorage.setItem("data", JSON.stringify(data))
  this.getContent()
}

function getContent() {

  var data = JSON.parse(sessionStorage.getItem("data"));

  if (data["model"]["hasConflicts"]) {
    document.getElementById("warning").classList.remove("w3-hide");
  }

  for (var i = 1; i <= Object.keys(data["teams"]).length; i++) {
    var team = data["teams"][i];
    teamNum = i
    createTeam(teamNum, team);
  }


}

function showMoveBanner(fullName, team_num) {
  $('#move-banner').show();
  document.getElementById("move-banner-message").innerHTML = `Move ${fullName} from team ${team_num} to team:`
}

function hideMoveBanner() {
  $('#move-banner').hide();
}

function generateDropDown(team_num) {

  $('#generateTeams')
    .find('option')
    .remove()
    .end();

  var data = JSON.parse(sessionStorage.data);
  var x = document.getElementById("generateTeams");
  var size = Object.size(data["teams"]);

  for (var i = 1; i <= size; i++) {
    if (i != team_num) {
      var option = document.createElement("option");
      option.text = i;
      x.add(option);
    }
  }
}

function moveMember() {
  var selectBox = document.getElementById("generateTeams");
  var newTeam = selectBox.options[selectBox.selectedIndex].value;
  var oldRow = document.getElementById("row-" + clickedID);
  var oldTeam = parseInt(oldRow.parentNode.id.replace("table-", ""));
  oldRow.parentNode.removeChild(oldRow);

  var newTeamTable = document.getElementById("table-" + newTeam);
  newTeamTable.appendChild(oldRow);

  var data = JSON.parse(sessionStorage.getItem("data"));

  var index = data["teams"][oldTeam]["members"].indexOf(clickedID);

  if (index != -1) {
    data["teams"][oldTeam]["members"].splice(index, 1);
    data["teams"][newTeam]["members"].push(clickedID);
  }

  sessionStorage.setItem("data", JSON.stringify(data))

  hideMoveBanner()
}

function findMovedMemberInfo(clicked) {
  var data = JSON.parse(sessionStorage.getItem("data"));

  var sel = document.getElementById("generateTeams");

  clickedID = clicked;

  console.log("student to move:" + clicked);

}

function getTeams() {
  return JSON.parse(sessionStorage.teams);
}

function getStudents() {
  return JSON.parse(sessionStorage.students);
}

function getIssues() {
  return JSON.parse(sessionStorage.issues);
}

function createTeam(team_num, team) {

  var data = JSON.parse(sessionStorage.getItem("data"));

  var row = document.createElement("div");
  row.setAttribute("class", "w3-cell-row row-team");
  var cell_team_members = document.createElement("div");
  cell_team_members.setAttribute("class", "w3-container w3-cell cell-team-members w3-card");
  var cell_divider = document.createElement("div");
  cell_divider.setAttribute("class", "w3-cell cell-divider");
  var cell_team_issues = document.createElement("div");
  cell_team_issues.setAttribute("class", "w3-container w3-cell cell-team-issues w3-card");
  row.appendChild(cell_team_members);
  row.appendChild(cell_divider);
  row.appendChild(cell_team_issues);

  var teamName = document.createElement("div");
  teamName.setAttribute("class", "card-name");
  teamName.innerHTML = "Team ".concat(team_num);
  cell_team_members.appendChild(teamName);

  var issueName = document.createElement("div");
  issueName.setAttribute("class", "card-name ");
  issueName.innerHTML = "Issues";
  cell_team_issues.appendChild(issueName);



  var table_members = document.createElement("table");

  table_members.setAttribute("id", "table-" + teamNum);
  console.log(table_members.id);
  table_members.setAttribute("class", "w3-table w3-bordered team-table");
  var header = document.createElement("tr");

  for (const header_text of ["ID", "Name", "GPA", "Gender", "Conflicts", "Move"]) {
    var header_cell = document.createElement("th");
    header_cell.innerHTML = header_text;
    header.appendChild(header_cell);
  }

  table_members.appendChild(header);

  for (const member of team["members"]) {

    var memberRow = document.createElement("tr");
    memberRow.setAttribute("id", "row-" + member);
    const member_data = data["people"][member]

    for (const memberCellIndex of ["id", "fullName", "gpa", "gender", "conflicts", ""]) {
      //create cell for each header and populate each 
      var memberCell = document.createElement("td");

      var firstName = member_data["firstName"];
      var lastName = member_data["lastName"];
      var fullName = firstName + " " + lastName;

      if (memberCellIndex != "" && memberCellIndex != "fullName") {
        memberCell.innerHTML = member_data[memberCellIndex];

      } else if (memberCellIndex == "fullName") {
        memberCell.innerHTML = fullName;
      }

      // to display the first and last name in the conflict column rather their userid

      var member_conflicts = ""

      if (memberCellIndex == "conflicts") {
        for (const member_conflict of member_data["conflicts"]) {
          var member_conflict_data = data["people"][member_conflict];

          var firstName = member_conflict_data["firstName"];
          var lastName = member_conflict_data["lastName"];
          var conflictFullName = firstName + " " + lastName + "<br>";
          member_conflicts = member_conflicts.concat(conflictFullName);
        }

        memberCell.innerHTML = member_conflicts;

      }
      memberRow.appendChild(memberCell);
    }
    for (const memberCellIndex of ["Move"]) {

      if (memberCellIndex != "") {

        var btn = document.createElement('input');
        btn.type = "button";
        btn.className = "btn btn-primary mb-2 mr-sm-2";
        btn.setAttribute("id", member);
        btn.setAttribute("onClick", `generateDropDown(${team_num}); showMoveBanner("${fullName}", ${team_num}); findMovedMemberInfo(this.id);`);
        btn.value = "move";
        memberCell.appendChild(btn);

      }
      memberRow.appendChild(memberCell);

    }
    table_members.appendChild(memberRow);


  }

  cell_team_members.appendChild(table_members);

  var container = document.getElementById("teams-container");
  container.appendChild(row);
}





function populate(team) {
  //make header row
  var element = document.getElementById(team);

  var table = document.createElement("table");
  table.setAttribute("class", "table");
  table.setAttribute("style", "table-layout: fixed");

  //initialize header row
  var head = document.createElement("THead");
  var tr = document.createElement("TR");
  var colHeaders = ["ID", "Name", "Acad", "Prog Skill", "Proj Skill", "Gender", "Conflicts", "Move"];
  for (var j = 0; j < colHeaders.length; j++) {
    var th = document.createElement("TH");
    th.setAttribute("scope", "col");
    th.style.width = "12.5%";
    th.appendChild(document.createTextNode(colHeaders[j]));
    tr.appendChild(th);
  }
  head.appendChild(tr);
  table.appendChild(head);
  element.appendChild(table);

  sortTeam(team); // sort by academic standing

  var teams = getTeams();
  var students = getStudents();

  //initialize tbody
  var body = document.createElement("tbody");
  var thisTeam = teams[team];

  for (var i = 0; i < thisTeam.length; i++) {
    var studentID = thisTeam[i]; //get a student from the team and store id
    //get student info
    var student = students[studentID]["name"];
    var gender = students[studentID]["gender"];
    var acad = students[studentID]["acad"];
    var conflict = students[studentID]["conflict"];

    // create move button for student
    var btn = document.createElement("BUTTON");
    btn.setAttribute("class", "btn btn-primary move-button");
    // set button onclick = showMoveBar('studentID-team#')
    btn.setAttribute("onClick", "showMoveBar('" + studentID + "-" + team + "')");
    btn.appendChild(document.createTextNode("move"));

    var btnBorder = document.createElement("TD");
    btnBorder.appendChild(btn);

    var studentAttributes = [studentID, student, gpa, gender, conflict];

    //create new TR element for this row
    var tr = document.createElement("TR");
    var th = document.createElement("TH");
    th.setAttribute("scope", "row");
    th.append(document.createTextNode(i + 1));
    th.appendChild(tr);

    //fill row with attributes
    for (k = 0; k < studentAttributes.length; k++) {
      var td = document.createElement("TD");
      if ((k !== 1) & (k !== 6)) {
        td.style.whiteSpace = "nowrap";
        td.style.overflow = "hidden";
        td.style.textOverflow = "ellipsis";
      }
      td.appendChild(document.createTextNode(studentAttributes[k]));
      tr.appendChild(td);
    }
    tr.appendChild(btnBorder); // add move button to student row
    body.appendChild(tr);
  }
  table.appendChild(body);
  element.appendChild(table);
}

function exportData() {

  var data = JSON.parse(sessionStorage.getItem("data"));
  console.log(data);

  var teamString = ""

  for (var i = 1; i <= Object.keys(data["teams"]).length; i++) {

    var team = data["teams"][i];

    teamString = teamString + "Team " + i + "\n";

    console.log("Team ".concat(i));

    for (const member of team["members"]) {
      var person = data["people"][member]
      console.log(member.concat(", ", person["firstName"], " ", person["lastName"]));

      teamString = teamString + person["id"] + "\t" + person["firstName"] + " " + person["lastName"] + "\n";
    }
    teamString = teamString + "\n"
  }

  console.log(teamString)
  console.log("works")
  return teamString;

}

function downloadTeams() {
  // //export teams to file when export button is clicked - group 5's way

  download("teams.txt", exportData())

  window.location.href = "export.html";

  //<a href="data:application/octet-stream;charset=utf-16le;base64,//5mAG8AbwAgAGIAYQByAAoA">text file</a>


}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
