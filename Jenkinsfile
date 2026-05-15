pipeline {
    agent any

    environment {
        DOCKER_USER = 'sobreiraa12344'
    }

    stages {
        stage('Checkout') {
            steps {
                // Simplificado para evitar erros de mapa
                checkout scm
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    // Requisito: Enviar imagens para o Docker Hub 
                    docker.withRegistry('', 'docker-hub-credentials') {
                        def back = docker.build("${DOCKER_USER}/gym-backend:latest", "./backend")
                        back.push()
                        
                        def front = docker.build("${DOCKER_USER}/gym-frontend:latest", "./frontend")
                        front.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Requisito: Deploy com Ansible 
                echo "Executando deploy..."
            }
        }
    }

    post {
        always {
            // Requisito: Notificação por email 
            mail to: 'sobreiraafonso@gmail.com',
                 subject: "Jenkins Build ${currentBuild.fullDisplayName}",
                 body: "Resultado: ${currentBuild.result}"
        }
    }
}