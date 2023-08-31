pipeline {
    agent any
    stages {
        stage('require') {
            steps {
                sh 'docker-compose -v'
            }
        }
        stage('setup') {
            steps {
                sh './task setup'
            }
        }
        stage('test') {
            steps {
                sh './task test'
            }
        }
    }
    post { 
        always {
            sh './task kill'
        }
    }
}