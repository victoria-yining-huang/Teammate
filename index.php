<!DOCTYPE html>
<html>
<style>
.w3-button{
 box-shadow: 0 20px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
 
}
a:hover {
  color: blue;
}
 #left{ 
        padding: 10px;
        float:left;  
        width:60%; 
        height:500px; 
} 
#right{ 
      
      float:right; 
      width:40%; 
      height:300px; 
      border-left: 3px solid;
      border-color: #FFD700 ;
      padding-left: 20px;

}


</style>
  <!-- CSS Classes -->
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css" />
  <link rel="stylesheet" type="text/css" href="www/main.css" />
  <!-- Fonts -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat" />
  <!-- Scripts -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script type="text/javascript" src="setup_script.js"></script>

  <body onload="uploadConflict();teamsize();uploadStudentFile();">
    <!-- Navbar -->
    <div class="w3-top">
      <div class="w3-bar w3-blue w3-card w3-left-align w3-large">
        <a href="#" class="w3-bar-item w3-button w3-padding-large w3-white">teammate</a>
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
            <div>
            <div id="left">
            <h3>Start the team generating process by:</h3>
            <h4>Upload the exported student data from 'Team 7 output' as a CSV file.</h4>
           <!-- <input type="file" id="student_data" />
            <button onclick="uploadStudentData()" class="w3-button w3-black w3-padding-large w3-large w3-margin-top">Upload Student Data</button>-->
            <input id="student_data" type="file" onchange="parseStudentData()"hidden/>
            <input id="student-buttonid" type="button" class="w3-button w3-black w3-padding-large w3-large w3-margin-top" value="Upload Student Data"/> 
            <div id="student-file-upload-filename"></div>
            <!--</form>-->
            <p id="student-error" style="color:red; font-weight: bold;"p>
            <p id="student-successful" style="color:green; font-weight: bold;" p>
            <br />
            <h4>See a sample table for the student data file.</h4>
            <h4><a href="data\students.csv" target="_blank" class="w3-margin-top"><b>
              Download Sample File</b></h4>
            </a>
  
            </div> 
            <!--- Adding instructions for page 1-->
          <div id= "right">
            <h3>Instructions</h3>
            
            <h5>1) Access the file given to you by Team-7.</h5>
            <h5>2) Make sure it is in <b>.csv</b> format.</h5>
            <h5>3) If you want to look at an example of a sample file, <br> download the sample file.</h5>
            <h5>4) Click on the upload button and select the Team-7 file.</h5>
            <h5>5) A Next Step button will appear, click on it.</h5>
          </div>
          </div>
          </div>
          <div class="w3-container w3-blue tab-footer page-footer">
            <button id="nextstep" class="w3-button w3-black w3-xlarge w3-hover-white" onclick="getNumStudents(student_data);nextTab('tab-1', 'tab-2')">
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
              
              <div id="left">
              <div>
                <span id="insertNumStudents" class="w3-xlarge"></span>
                <span class="w3-xlarge"> students found in the inputted file.</span>
              </div>

              <p class="w3-xlarge"><b>Configure:</b></p>
              <p class="w3-xlarge">Please enter the number of members per team</p>
              <p class="w3-xlarge">Team Size: <input type="number" min="0" id="teamSize" step="1" required="required" oninput="getNumTeams(numStudents)" 
             onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57"/></p>
              
              <div class="w3-margin-top">
                <span class="w3-xlarge">Number of Teams: </span>
                <span class="w3-xlarge" id="insertNumTeams"></span>
              </div>

            </div>
             <div id= "right">
            <h3>Instructions</h3>
            
            <h5>1) Check if the number of students in the uploaded file is same as the one displayed on the top of the page.</h5>
            <h5>2) Enter the desired team size. The value that you enter is the minimum number of students that would be placed within a team. If the number of students cannot be divided evenly within the entered team size, then some teams may have <b>team size +1</b> students. </h5>
            <h5>3) The number of teams for the model will be calculated and displayed below the text field! </h5>
          </div>
          </div>
          </div>

          <div class="w3-container w3-blue tab-footer page-footer">
            <button class="w3-button w3-black w3-xlarge w3-hover-white" onclick="nextTab('tab-2', 'tab-1')">
              Previous Step
            </button>
            <button id = "size-nextstep" class="w3-button w3-black w3-xlarge w3-hover-white" onclick="nextTab('tab-2', 'tab-3')">
              Next Step
            </button>
          </div>
        </div>
        <div id="tab-3" class="hidden">
          <div class="w3-container tab-header w3-center">
            <h3>Upload Student Conflicts</h3>
          </div>
          <div class="w3-container tab-content">
          <div id ="left">
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
            <a href="data\conflicts.csv" target="_blank" class="w3-margin-top"><b><h4>
              Download Sample File</h4></b>
            </a>
            <br>
           <!---Constraints-->
           <h4>Would you like to include the following constraints for generating teams? <br>Select ALL that apply.</h4> 
          <div>
            <input type="checkbox" id="gender" name="constraints" value="gender" checked>
            <label for="gender">Gender</label>
          </div>

          <div>
            <input type="checkbox" id="GPA" name="constraints" value="GPA" checked>
            <label for="GPA">GPA</label>
          </div>


          <input id="buttonid" type="button" class="w3-button w3-black w3-padding-large w3-large w3-margin-top" value="Submit" onclick="pass_constraints()"/>
          </div>

          <div id= "right">
            <h3>Instructions</h3>
            <h5>1) Click the upload conflict button. </h5>
            <h5>2) Find the conflicts file provided to you by Team-7 and click <b>Open</b>.</h5>
            <h5>2) Make sure it is in <b>.csv</b> format.</h5>
            <h5>3) If you want to look at an example of a sample file, <br> download the sample file.</h5>
            <h5>4) Click on the upload button and select the Team-7 file.</h5>
            <h5>5) A Generate Teams button will appear, click on it.</h5>
          </div>

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
