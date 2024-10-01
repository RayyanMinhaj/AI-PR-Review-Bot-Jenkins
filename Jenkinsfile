pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('GITHUB_TOKEN') 
        OPENAI_API_KEY = credentials('OPENAI_API_KEY')
    }


    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    bat 'npm install'
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    bat 'npx tsc' // compiles TypeScript to JavaScript
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
                        bat 'node dist/index.js > git_diff.txt'
                    }
                }
            }
        }
    }
}
