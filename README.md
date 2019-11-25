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
