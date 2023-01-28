pipeline {
    agent {
        docker {
            image '352708296901.dkr.ecr.eu-west-2.amazonaws.com/schiff-jenkins-new-agent:latest'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
           stage('Clone') {
               steps {
                   sh 'git clone https://github.com/JohnSchiff/DevOps_project.git'
               }
           }
           stage('Build') {
               steps {
                   sh 'docker build -t webapp .'
               }
           }
           stage('Run') {
               steps {
                   sh 'docker run -p 8501:8501 webapp'
               }
           }
       }
   }