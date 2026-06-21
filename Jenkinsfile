pipeline {
    agent any

    environment {
        IMAGE_NAME = "aariskazi/leaderboard"
        CONTAINER_NAME = "leaderboard"
        PORT = "8081"
        IMAGE_TAG = "v${BUILD_NUMBER}"
        PYTHONDONTWRITEBYTECODE=1
        PYTHONUNBUFFERED=1
    }

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Aaris-Kazi/LeaderBoards.git'
            }
        }

        stage('Debug') {
            steps {
                sh 'ls -la'
                sh 'find . -name requirements.txt'
                sh 'find . -name Dockerfile'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop $CONTAINER_NAME || true'
                sh 'docker rm $CONTAINER_NAME || true'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                    --env-file .env \
                    --name $CONTAINER_NAME \
                    -p 8086:$PORT \
                    ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }
}