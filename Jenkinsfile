pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'joaodiofonse'
        IMAGE_BACKEND   = "${DOCKERHUB_USER}/gymnasium-backend"
        IMAGE_FRONTEND  = "${DOCKERHUB_USER}/gymnasium-frontend"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/b01-b01/gymnasium.git'
            }
        }

        stage('Build Backend') {
            steps {
                sh 'docker build -t $IMAGE_BACKEND ./backend'
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t $IMAGE_FRONTEND ./frontend'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $IMAGE_BACKEND'
                    sh 'docker push $IMAGE_FRONTEND'
                }
            }
        }

    }

    post {
        success {
            mail to: 'joaodiogofonseca01@gmail.com',
                 subject: "Pipeline OK - Gymnasium",
                 body: "O pipeline correu com sucesso!"
        }
        failure {
            mail to: 'joaodiogofonseca01@gmail.com',
                 subject: "Pipeline FALHOU - Gymnasium",
                 body: "O pipeline falhou. Verifica o Jenkins para mais detalhes."
        }
    }
}