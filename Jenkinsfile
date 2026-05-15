pipeline {
    agent any

    environment {
        DOCKER_USER = 'sobreiraa12344'
        FRONT_IMAGE = "${DOCKER_USER}/gym-frontend"
        BACK_IMAGE = "${DOCKER_USER}/gym-backend"
    }

    stages {
        stage('Checkout') {
            steps {
                // Forma mais robusta de fazer checkout no Jenkins
                git branch: 'main', url: 'https://github.com/b01-b01/gymnasium' [cite: 17]
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    // Requisito: Imagens Docker para Front e Back 
                    docker.withRegistry('', 'docker-hub-credentials') {
                        
                        // Build do Backend
                        def backend = docker.build("${BACK_IMAGE}:latest", "./backend")
                        backend.push()

                        // Build do Frontend
                        def frontend = docker.build("${FRONT_IMAGE}:latest", "./frontend")
                        frontend.push()
                    }
                }
            }
        }

        stage('Deploy com Ansible') {
            steps {
                // Requisito: Deploy automático [cite: 18]
                echo "A preparar deploy com Ansible..."
            }
        }
    }

    post {
        always {
            // Requisito: Notificação por email 
            emailext body: "O build ${env.BUILD_ID} terminou com: ${currentBuild.result}",
                     subject: "Status: ${currentBuild.fullDisplayName}",
                     to: 'sobreiraafonso@gmail.com' [cite: 12, 13]
        }
    }
}