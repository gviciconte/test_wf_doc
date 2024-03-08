# How to set up a case in the CI/CD server

Once your IP address has been cleared by DCS (you should send a email to augusto.moura@dcs-computing.com), you will be able to access the jenkins server and set up the tests.

## Jenkins main page
Jenkins has a web-based graphical interface for setting up and handling cases. 
The main page after logging in is below, where you can select **New Item** to start setting up the case.

![Alt text](jenkins_project_setup_instructions/Slide2.PNG?raw=true "Title")


## Select Freestyle project
![Alt text](jenkins_project_setup_instructions/Slide3.PNG?raw=true "Title")

## Setting up the case
In the tabs here you can set up the details of the test case. For a simple case you only need a description if desired...

![Alt text](jenkins_project_setup_instructions/Slide4.PNG?raw=true "Title")

... And the repository where the project is located. Be sure to use the SSH link for the repository (git@github.com) and set SSH key for github checkout.

![Alt text](jenkins_project_setup_instructions/Slide5.PNG?raw=true "Title")

### Build triggers

In the Build Triggers tab you can define how the project is built. In the example, it is done once per day.

![Alt text](jenkins_project_setup_instructions/Slide6.PNG?raw=true "Title")

### Build Environment

In Build Environment you set the building steps. In the example, a simple bash script to execute the case selected with `Execute Shell`

![Alt text](jenkins_project_setup_instructions/Slide7.PNG?raw=true "Title")

## Project page

![Alt text](jenkins_project_setup_instructions/Slide8.PNG?raw=true "Title")

## information on the execution
![Alt text](jenkins_project_setup_instructions/Slide10.PNG?raw=true "Title")
