// Script file for HTML page: generate_teams.html

window.onload = function generateTeams() {
  console.log("RUNNING")
  console.log(sessionStorage.getItem('students'))

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
    success: function(obj, textstatus) {
      if (!("error" in obj) && !(obj == null)) {
        console.log(obj.result)

        var index = fruits.indexOf("json_result_output");
        data = JSON.parse(obj.result[index + 1]);
        
        sessionStorage.setItem('output', data);
        //window.location.href = "teams.html";
      } else {
        console.log(obj.error);
      }
    }
  });
}
