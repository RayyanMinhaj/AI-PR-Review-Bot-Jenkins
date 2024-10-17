pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('GITHUB_TOKEN') 
        OPENAI_API_KEY = credentials('OPENAI_API_KEY')
        GMAIL_APP_PASS = credentials('GMAIL_APP_PASS')
        DESTINATION_BRANCH = 'main'
    }

    stages {
        stage('Check PR Destination Branch') {
            steps {
                script {
                    // Check if the PR is into the desired destination branch
                    if (${env.GITHUB_PR_DESTINATION_BRANCH} != DESTINATION_BRANCH) {
                        echo "Skipping pipeline as the PR is NOT into ${DESTINATION_BRANCH}"
                        currentBuild.result = 'SUCCESS'
                        return // Exit the pipeline early if branch does not match
                    }
                }
            }
        }

        stage('Pull and Run Docker Image') {
            steps {
                script {              
                    bat 'docker pull rayyanm22/ai-pr-bot:latest'

                    bat """
                        docker run \
                        -e GITHUB_TOKEN=${GITHUB_TOKEN} \
                        -e GITHUB_PR_SOURCE_REPO_OWNER=${env.GITHUB_PR_SOURCE_REPO_OWNER} \
                        -e OPENAI_API_KEY=${OPENAI_API_KEY} \
                        -e GMAIL_APP_PASS=${GMAIL_APP_PASS} \
                        -e GITHUB_REPO_GIT_URL=${GITHUB_REPO_GIT_URL} \
                        -e GITHUB_PR_NUMBER=${GITHUB_PR_NUMBER} \
                        -e DECIDER="GitHub" \
                        rayyanm22/ai-pr-bot:latest
                    """
                }
            }
        }

        
    }   
}
