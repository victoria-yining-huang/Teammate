// Script file for HTML page: view_group.html
var dataStr;
var data;
var clickedID;
var teamNum;
var oldTeam;

// Get the size of an object
Object.size = function (obj) {
  var size = 0, key;
  for (key in obj) {
    if (obj.hasOwnProperty(key)) size++;
  }
  return size;
};

window.onload = function () {

  //sets the JSON object to a data hashmap

  data = JSON.parse(sessionStorage.getItem('output'));
  this.sessionStorage.setItem("data", JSON.stringify(data))
  this.getContent()

  //removed the workaround for server errors
  // $.ajax({
  //   url: "/get-sample-output",
  //   type: "get",
  //   success: function (resp) {
  //     sessionStorage.setItem("data", JSON.stringify(resp));
  //     getContent();
  //   }
  // });
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

getConflictIssues();
}

function showMoveBanner(fullName) {
  var data = JSON.parse(sessionStorage.getItem("data"));
  $('#move-banner').show();
  console.log(oldTeam)
  document.getElementById("move-banner-message").innerHTML = "Move "+ `${fullName} from team `+ oldTeam +" "+ "to team:"
}

function hideMoveBanner() {
  $('#move-banner').hide();
}

function generateDropDown() {

  $('#generateTeams')
    .find('option')
    .remove()
    .end();


  var data = JSON.parse(sessionStorage.getItem("data"));
  var x = document.getElementById("generateTeams");
  var size = Object.size(data["teams"]);

  for (var i = 1; i <= size; i++) {
    if (i != oldTeam) {
      var option = document.createElement("option");
      option.text = i;
      x.add(option);
    }
  }


}

function moveMember() {
  var data = JSON.parse(sessionStorage.getItem("data"));
  var selectBox = document.getElementById("generateTeams");
  var newTeam = selectBox.options[selectBox.selectedIndex].value;
  var oldRow = document.getElementById("row-" + clickedID);
  //var oldTeam = parseInt(oldRow.parentNode.id.replace("table-", ""));
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

  hideMoveBanner();
  getConflictIssues();

}

function findMovedMemberInfo(clicked) {
  var data = JSON.parse(sessionStorage.getItem("data"));

  var sel = document.getElementById("generateTeams");

  clickedID = clicked;
  var oldRow = document.getElementById("row-" + clickedID);
  oldTeam = parseInt(oldRow.parentNode.id.replace("table-", ""));
  console.log("ot"+oldTeam)

  console.log("student to move:" + clicked);

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
  cell_team_issues.setAttribute("id", "issueBox-" + teamNum);
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

  for (const header_text of ["ID", "Name", "GPA", "Conflicts", "Move"]) {
    var header_cell = document.createElement("th");
    header_cell.innerHTML = header_text;
    header.appendChild(header_cell);
  }

  table_members.appendChild(header);

  for (const member of team["members"]) {

    var memberRow = document.createElement("tr");
    memberRow.setAttribute("id", "row-" + member);
    const member_data = data["people"][member]

    for (const memberCellIndex of ["id", "fullName", "gpa", "conflicts", ""]) {
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
        btn.setAttribute("onClick", `findMovedMemberInfo(this.id);generateDropDown(); showMoveBanner("${fullName}"); `);
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


function exportData() {

  var data = JSON.parse(sessionStorage.getItem("data"));

  var teamString = ""

  for (var i = 1; i <= Object.keys(data["teams"]).length; i++) {

    var team = data["teams"][i];

    //adds column headings for the exported file
    if (i == 1) {
      teamString = "user_id" + "," + "First Name" + "," + "Last Name" + "," + "e-mail" + "," + "GPA" + "," + "Team" + "\n"
    }

    for (const member of team["members"]) {
      var person = data["people"][member]

      //the columns printed
      teamString = teamString + person["id"] + "," + person["firstName"] + "," + person["lastName"] + "," + person["email"] + "," + person["gpa"] + "," + i + "\n";
    }

    //teamString = teamString + "\n"
  }

  return teamString;

}

function downloadTeams() {
  // //export teams to file when export button is clicked - group 5's way

  download("teams.csv", exportData())

  window.location.href = "export.html";

}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

//----------------------------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------------------------
//---------------------------------------- these are for the issue box -------------------------------------------
//----------------------------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------------------------

function getFullName(id) {
  var data = JSON.parse(sessionStorage.getItem("data"));
  var firstName = data['people'][id]["firstName"];
  var lastName = data['people'][id]["lastName"];
  var fullName = firstName + " " + lastName;
  return fullName;
}


function getConflictIssues(){

$("p").remove();
// this finds the people who are in top and bottom tiers of GPA
// top/bottom tier: top/bottom n GPAs (including duplicated values), where n = number of teams
    var data = JSON.parse(sessionStorage.getItem("data"));
    var n = Object.size(data["teams"]);
    console.log(n)
    gpa = [];
     for (var team in data['teams']) {
        var membersOfTeam = data['teams'][Object.values(team)];
        for (var j = 0; j < data['teams'][Object.values(team)]['members'].length; j++) {
            student = data['people'][membersOfTeam['members'][j]];
            gpa.push(student["gpa"]);
     }
}
   gpa.sort(function(a, b){return b-a});

    var top = gpa.slice(0, n);
    var bottom = gpa.slice((gpa.length - n), gpa.length);
    console.log("gpa" + gpa);
    console.log("top" + top);
    console.log("bottom" + bottom);

//now begins personal conflict
    conflict = [];




  var data = JSON.parse(sessionStorage.getItem("data"));
  for (var team in data['teams']) {
    var conflictString = "";

    var membersOfTeam = data['teams'][team];

    for (var j = 0; j < data['teams'][team]['members'].length; j++) {
      student = data['people'][membersOfTeam['members'][j]];

      for (t = 0; t < student['conflicts'].length; t++) {
        conflict = [];

         if (membersOfTeam['members'].includes(student['conflicts'][t])){
             console.log("student" + getFullName(student["id"]) + " has a conflict with " + getFullName(student['conflicts'][t]))
             var conflictString = getFullName(student["id"]) + " has a conflict with " + getFullName(student['conflicts'][t])
             var para = document.createElement("p");
            para.innerHTML = conflictString;
            console.log(conflictString)
            document.getElementById("issueBox-" + team).appendChild(para);
         }
    }



    }
}
for (var team in data['teams']) {
    var hasTop = false;
    var hasBott = false;
    var membersOfTeam = data['teams'][Object.values(team)];
      for (var j = 0; j < data['teams'][Object.values(team)]['members'].length; j++) {
        student = data['people'][membersOfTeam['members'][j]];
        console.log("student is " + student["id"])
        if (top.includes(student["gpa"])) {
            hasTop = true;
            }
        if (bottom.includes(student["gpa"])) {
            hasBott = true;
            }
           }
        if (hasTop == false) {
        st = "This team is missing a top tier student"
        console.log("team" + team + "is missing a top tier student")

        var para = document.createElement("p");
        para.innerHTML = st;
        document.getElementById("issueBox-" + team).appendChild(para);
        }
        if (hasBott == false) {
        st = "This team is missing a bottom tier student"
        console.log("team" + team + "is missing a bottom tier student")

        var para = document.createElement("p");
        para.innerHTML = st;
        document.getElementById("issueBox-" + team).appendChild(para);
        }

}

}

