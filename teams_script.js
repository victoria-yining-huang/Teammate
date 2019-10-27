// Script file for HTML page: view_group.html

// $.getJSON("data/output.json", function(json) {
//   data = json;
//   console.log(data);
//   getContent();
// });

window.onload = function() {
  data = JSON.parse(sessionStorage.getItem('output'));
  this.getContent(data)
}

function getContent(data) {

  if (data["model"]["hasConflicts"]) {
    document.getElementById("warning").classList.remove("w3-hide");
  }

  for (var i = 1; i <= Object.keys(data["teams"]).length; i++) {
    var team = data["teams"][i];
    createTeam(i, team);
  }
}

function createTeam(team_num, team) {
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
  table_members.setAttribute("class", "w3-table w3-bordered team-table");
  var header = document.createElement("tr");
  
  for (const header_text of ["ID", "Name", "Acad", "Prog Skill", "Proj Skill", "Gender", "Conflicts", "Move"]) {
    var header_cell = document.createElement("th");
    header_cell.innerHTML = header_text;
    header.appendChild(header_cell);
  }

  table_members.appendChild(header);

  for (const member of team["members"]) {
    var memberRow = document.createElement("tr");
    const member_data = data["people"][member]

      for (const memberCellIndex of ["id", "firstName", "", "", "", "", "conflicts", ""]) {
      //create cell for each header and populate each 
        var memberCell = document.createElement("td");
        
        if (memberCellIndex != "") {
            memberCell.innerHTML = member_data[memberCellIndex];
        }
      memberRow.appendChild(memberCell);
     }
  table_members.appendChild(memberRow);
}

  cell_team_members.appendChild(table_members);

  var container = document.getElementById("teams-container");
  container.appendChild(row);
}

function temp() {
  //create row for each team
  for (i = 0; i < teamNamesArray.length; i++) {
    if (teamNamesArray[i] !== "teamCount") {
      var testElement = document.getElementById("test");
      var row = document.createElement("div");
      row.setAttribute("class", "row");
      row.style.marginTop = "1%";
      row.style.marginBottom = "1%";
      testElement.appendChild(row);

      //column for team data
      var teamColumn = document.createElement("div");
      teamColumn.setAttribute("class", "col-sm-8");
      row.appendChild(teamColumn);

      //create team card and populate it
      var teamCard = document.createElement("div");
      teamCard.setAttribute("class", "card");
      teamCard.style.boxShadow = "0 10px 6px -6px #BBBBBB";
      teamColumn.appendChild(teamCard);

      var teamCardHeader = document.createElement("div");
      teamCardHeader.setAttribute("class", "card-header");
      var teamName = document.createTextNode("Team " + i);
      teamCardHeader.appendChild(teamName);
      teamCard.appendChild(teamCardHeader);

      var teamTable = document.createElement("div");
      teamTable.setAttribute("class", "container");
      teamCard.appendChild(teamTable);

      var teamMembers = document.createElement("ul");
      teamMembers.setAttribute("id", teamNamesArray[i]);
      teamMembers.setAttribute("class", "list-group list-group-flush");
      teamTable.appendChild(teamMembers);
      populate(teamNamesArray[i]);

      //column for conflict data
      var conflictsColumn = document.createElement("div");
      conflictsColumn.setAttribute("class", "col-sm-4");
      row.appendChild(conflictsColumn);

      //create conflict card and populate it
      var conflictsCard = document.createElement("div");
      conflictsCard.setAttribute("class", "card");
      conflictsCard.style.boxShadow = "0 10px 6px -6px white";
      conflictsCard.style.height = "100%";
      conflictsColumn.appendChild(conflictsCard);

      var conflictsHeader = document.createElement("div");
      conflictsHeader.setAttribute("class", "card-header");
      var conflictName = document.createTextNode("Conflicts");
      conflictsHeader.appendChild(conflictName);
      conflictsCard.appendChild(conflictsHeader);

      var conflictsBody = document.createElement("div");
      conflictsBody.setAttribute("class", "card-body");
      var conflicts = showIssues(teamNamesArray[i]);
      conflictsBody.appendChild(conflicts);
      conflictsCard.appendChild(conflictsBody);
    }
  }
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
    var prog = students[studentID]["prog"];
    var proj = students[studentID]["proj"];
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

    var studentAttributes = [studentID, student, acad, prog, proj, gender, conflict];

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
