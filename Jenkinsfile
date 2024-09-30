pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('GITHUB_TOKEN') 
    }


    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    
                    withEnv(["PATH+NODE=${tool name: 'NodeJS', type: 'NodeJS'}/bin"]) {
                        sh 'npm install' 
                    }
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    withEnv(["PATH+NODE=${tool name: 'NodeJS', type: 'NodeJS'}/bin"]) {
                        sh 'npx tsc' // compiles TypeScript to JavaScript
                    }
                }
            }
        }
        stage('Post Comment') {
            steps {
                script {
                    withEnv([
                        "GITHUB_PR_SOURCE_REPO_OWNER=${env.GITHUB_PR_SOURCE_REPO_OWNER}",
                        "GITHUB_REPO_GIT_URL=${env.GITHUB_REPO_GIT_URL}",
                        "GITHUB_PR_NUMBER=${env.GITHUB_PR_NUMBER}",
                        "GITHUB_TOKEN=${env.GITHUB_TOKEN}"
                    ]) { 
                        bat 'node dist/index.js'
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
