# Teammate Documentation

## Data Disclaimer

> **WARNING**: The application should (and can) be run locally if sensitive student data is being uploaded. Refer to the _Setup the Development Environment_ section for instructions.

## Deploy the Application

To deploy the application on Heroku, follow these steps:

1. Create a new Heroku application
2. Under the Settings tab, add Python as the buildpack under Buildpacks
3. Under the Deploy tab, select master as our branch to deploy, then deploy the branch

## Setup the Development Environment

To setup a development environment

1. Clone the GitHub repository to your local device
2. Using the terminal, open the root folder of the project
3. Run the command `flask run` to launch Flask on a local port
4. Open the local host address to

If an error occurs when attempting to run the model on a new local device, there is likely an issue related to your local environment and the Python multiprocessing module. Please refer to these guides:

[Windows]()
[Mac]()
