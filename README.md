# Teammate Documentation

## Data Disclaimer

> **WARNING**: It is highly recommended to run the application locally if sensitive student data is being uploaded. Refer to the _Setup the Development Environment_ section for instructions.

The application temporarily stores data in both your browser session storage and server memory. Personal identifiable information (first name, last name, user id) of the data is only used locally for display purposes, and does not get sent to the server. The model receives the data as student 1, 2, ... , n and returns the team assignments of student 1, 2, ... , n, which is then attached to the corresponding students data.

In addition, every instance of the model is protected using a client session-specific key, assigned when the model is started, which prevents any requests to the server from accessing a model that did not originate from the client session that initiated the model.

## Deploy the Application

To deploy the application on Heroku, follow these steps:

1. Create a new Heroku application
2. Under the Settings tab, add Python as the buildpack under Buildpacks
3. Under the Deploy tab, select master as our branch to deploy, then deploy the branch

## Setup the Development Environment

To setup a development environment, follow these steps:

1. Clone the GitHub repository to your local device
2. Ensure your computer has Python 3 installed
3. Install the Python packages listed in the `requirements.txt` file located in the root folder of the project
4. Using the terminal, open the root folder of the project
5. Run the command `flask run` to launch Flask on a local port
6. Open the local host address in a browser to view the deployed application

## Usage Instructions
1. Open the deployed Heroku app or the local development environment
2. Access the Student Data file provided by Team 7 or download a sample Student Data file using the 'Download Sample File' button
3. Click on the 'Upload Student Data' button and upload the Student Data file ensuring that the file is in .CSV format and has the correct header columns. If the uploaded file is not in an acceptable format, error messages will appear to assist
4. Upon an upload of the correct Student Data file, click the 'Next Step' button in the bottom right hand corner
5. Ensure that the number of students found in the inputted file is correct
6. Enter the preferred team size. The system will not accept negative integers, floats, or numbers larger than the total number of students found
7. After entering an accepted team size, click the 'Next Step' button
8. Select the GPA checkbox if you want to distribute students based on their GPA, otherwise only student conflicts will be taken into account
9. Click the 'Next Step' button
10. Access the Conflict Data file provided by Team 7 or download a sample Conflict Data file using the 'Download Sample File' button
11. Click on the 'Upload Conflict Data' button and upload the Conflict Data file ensuring that the file is in .CSV format and has the correct header columns. If the uploaded file is not in an acceptable format, error messages will appear to assist
12. Upon an upload of the correct Conflict Data file, click the 'Generate Teams' button in the bottom right hand corner
13. On the Teams page, view the generated teams based on the uploaded files and team size specifications
14. If you wish to move a member of a team, click on the move button next to the students name and specify which team to move them to in the displayed drop down
15. The personal conflicts within each team will be populated in the issue boxes. These will be updated after moving each member.
16. Click submit to move the student
17. When ready to export the generated teams, click the 'Export Teams' button where a file names 'teams.csv' will download to your local computer
18. Click the 'Return to Start' button to return to the start of teammate.
