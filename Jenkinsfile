pipeline {
    agent any 
    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    bat 'npm install'
                }
            }
        }
        stage('Compile TypeScript') {
            steps {
                script {
                    bat 'npx tsc'
                }
            }
        }
        stage('Run Application') {
            steps {
                script {
                    bat 'node dist/index.js'
                }
            }
        }
    }
}
