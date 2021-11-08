pipeline {
    agent any
    
    stages {
        stage('Checkout'){
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '**']], extensions: [], userRemoteConfigs: [[credentialsId: 'g1t7', url: 'git@github.com:pandaponn/IS212_G1T7.git']]])
            }
        }
        stage('Code_Analysis'){
            steps {
                sh '''
                python3 -m venv env 
                source env/bin/activate 
                pip3 install flake8 
                flake8 src/app.py
                '''
            }
        }
        stage('Testing'){
            steps {
                sh '''
                python3 -m venv env 
                source env/bin/activate
                pip3 install flask flask_sqlalchemy flask_cors datetime
                python3 services/unit_test.py
                '''
            }
        }
    }
}