// Script file for HTML page: generate_teams.html

window.onload = function generateTeams() {
  console.log("RUNNING")
  console.log(sessionStorage.getItem('students'))
  console.log(sessionStorage.getItem('conflicts'))
  console.log(sessionStorage.getItem('team_size'))

  jQuery.ajax({
    type: "POST",
    url: "server.php",
    dataType: "json",
    data: {
      functionname: "generate",
      arguments: {
        students: sessionStorage.getItem('students'),
        conflicts: sessionStorage.getItem('conflicts'),
        team_size: sessionStorage.getItem('team_size')
      }
    },
    success: function (obj, textstatus) {
      if (!("error" in obj) && !(obj == null)) {
        console.log(obj.result)

        if (!obj.result.includes("python_error")) {
          var index = obj.result.indexOf("json_result_output");
          sessionStorage.setItem('output', obj.result[index + 1]);
          window.location.href = "teams.html";
        }
      } else {
        console.log(obj.error);
      }
    }
  });
}
