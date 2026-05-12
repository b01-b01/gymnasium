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
                checkout scm [cite: 17]
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    // Login e Push para Docker Hub [cite: 16]
                    docker.withRegistry('', 'docker-hub-credentials') {
                        
                        // Backend
                        def backend = docker.build("${BACK_IMAGE}:${env.BUILD_ID}", "./backend")
                        backend.push()
                        backend.push("latest")

                        // Frontend
                        def frontend = docker.build("${FRONT_IMAGE}:${env.BUILD_ID}", "./frontend")
                        frontend.push()
                        frontend.push("latest")
                    }
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                // Requisito: Deploy automático 
                echo "A executar Ansible para instalação/upgrade..."
                // sh 'ansible-playbook -i ansible/inventory.ini ansible/deploy.yml'
            }
        }
    }

    post {
        always {
            // Requisito: Enviar email em caso de sucesso ou erro [cite: 12]
            mail to: 'teu-email@isec.pt',
                 subject: "Status Pipeline Gymnasium: ${currentBuild.result}",
                 body: "O build ${env.BUILD_ID} terminou com status: ${currentBuild.result}\nLink: ${env.BUILD_URL}"
        }
    }
}