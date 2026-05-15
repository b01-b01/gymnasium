pipeline {
    agent any

    environment {
        DOCKER_USER = 'joaodiofonse'
        DOCKER_CREDS_ID = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CREDS_ID}") {
                        def back = docker.build("${DOCKER_USER}/gymnasium-backend:latest", "./backend")
                        back.push()
                        def front = docker.build("${DOCKER_USER}/gymnasium-frontend:latest", "./frontend")
                        front.push()
                    }
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                ansiblePlaybook playbook: 'ansible/deploy.yml', inventory: 'ansible/inventory.ini'
            }
        }
    }

    post {
        success {
            mail to: 'joaodiogofonseca01@gmail.com',
                 subject: "✅ Pipeline OK - Gymnasium",
                 body: "O pipeline correu com sucesso!\nURL: ${env.BUILD_URL}"
        }
        failure {
            mail to: 'joaodiogofonseca01@gmail.com',
                 subject: "❌ Pipeline FALHOU - Gymnasium",
                 body: "O pipeline falhou.\nURL: ${env.BUILD_URL}"
        }
    }
}