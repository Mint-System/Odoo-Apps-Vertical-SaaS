pipeline {
    agent any
    stages {
        stage('require') {
            steps {
                sh 'docker-compose -v'
            }
        }
        stage('test') {
            steps {
                sh './task all'
            }
        }
    }
}