<!DOCTYPE html>
<html>
  <!-- CSS Classes -->
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css" />
  <link rel="stylesheet" type="text/css" href="www/main.css" />
  <!-- Fonts -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat" />
  <!-- Scripts -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script type="text/javascript" src="setup_script.js"></script>

  <body onload="uploadConflict()">
    <!-- Navbar -->
    <div class="w3-top">
      <div class="w3-bar w3-blue w3-card w3-left-align w3-large">
        <a href="#" class="w3-bar-item w3-button w3-padding-large w3-white">teammate</a>
        <a href="#" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Instructions</a>
      </div>
    </div>

    <!-- Page Content -->
    <div class="page-content">
      <div class="w3-container w3-blue w3-center">
        <h1>Setup</h1>
      </div>
      <div id="tabs" class="w3-container">
        <div id="tab-1">
          <div class="w3-container tab-header w3-center">
            <h3>Upload Student Data</h3>
          </div>
          <div class="w3-container tab-content">
            <h3>Start the team generating process by:</h3>
            <h5>Upload the exported student data from 'Team 7 output' as a CSV file.</h5>
            <input type="file" id="student_data" />
            <button onclick="uploadStudentData()" class="w3-button w3-black w3-padding-large w3-large w3-margin-top">Upload Student Data</button>
            <br />
            <h5>See a sample table for the student data file.</h5>
            <a href="data\students.csv" target="_blank" class="w3-margin-top">
              Download Sample File
            </a>
            <!--	<br> <h5>2) Uploading an existing team file as a .xlsx file</h5> -->
            <!--	
            	<input type="file" id="student_data"/>
            	<button onclick="upload()"class="w3-button w3-black w3-padding-large w3-large w3-margin-top">Upload</button>
            -->
          </div>
          <div class="w3-container w3-blue tab-footer page-footer">
            <button class="w3-button w3-black w3-xlarge w3-hover-white" onclick="getNumStudents(student_data);nextTab('tab-1', 'tab-2')">
              Next Step
            </button>
          </div>
        </div>
        <div id="tab-2" class="hidden">
          <div>
            <div class="w3-container tab-header w3-center">
              <h3>Configure Teams</h3>
            </div>
            <div class="w3-container tab-content">
              <div>
                <span id="insertNumStudents" class="w3-xlarge"></span>
                <span class="w3-xlarge"> students found in the inputted file.</span>
              </div>
              <p class="w3-xlarge"><u>Configure: </u></p>
              <p class="w3-xlarge">Please enter the number of members per team</p>
              <p class="w3-xlarge">Team Size: <input type="number" min="1" id="teamSize" step="1" required="required" /></p>
              <button class="w3-button w3-black w3-padding-large w3-large w3-margin-top" onclick="getNumTeams(numStudents)">Calculate Number of Teams</button>
              <div class="w3-margin-top">
                <span class="w3-xlarge">Number of Teams: </span>
                <span class="w3-xlarge" id="insertNumTeams"></span>
              </div>
            </div>
          </div>
          <div class="w3-container w3-blue tab-footer page-footer">
            <button class="w3-button w3-black w3-xlarge w3-hover-white" onclick="nextTab('tab-2', 'tab-1')">
              Previous Step
            </button>
            <button class="w3-button w3-black w3-xlarge w3-hover-white" onclick="nextTab('tab-2', 'tab-3')">
              Next Step
            </button>
          </div>
        </div>
        <div id="tab-3" class="hidden">
          <div class="w3-container tab-header w3-center">
            <h3>Upload Student Conflicts</h3>
          </div>
          <div class="w3-container tab-content">
            <h5>Please upload the conflict file generated by Team 7 as a CSV file.</h5>
            <!--<form id="formid" name="form" method="post" action="upload.php" enctype="multipart/form-data" >-->
              <input id="conflict_data" type="file" name="my_file" hidden/>
              <input id="buttonid" type="button" class="w3-button w3-black w3-padding-large w3-large w3-margin-top" value="Upload Conflict File" onclick="readConflicts()"/> 
              <div id="file-upload-filename"></div>
            <!--</form>-->
            <p id="error" style="color:red; font-weight: bold;"p>
            <p id="successful" style="color:green; font-weight: bold;" p>
            <br />
            <h5>See a sample table for the student conflict file.</h5>
            <a href="data\conflicts.csv" target="_blank" class="w3-margin-top">
              Download Sample File
            </a>
          </div>
          <div class="w3-container w3-blue tab-footer page-footer">
            <button class="w3-button w3-black w3-xlarge w3-hover-white" onclick="nextTab('tab-3', 'tab-2')">
              Previous Step
            </button>
            <button id="generate" class="w3-button w3-black w3-xlarge w3-hover-white" onclick="generateTeams()">
              Generate Teams
            </button>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>