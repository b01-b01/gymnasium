pipeline {
    agent any

    environment {
        DOCKER_USER = 'sobreiraa12344'
        // IDs das credenciais que criaste no Jenkins
        DOCKER_CREDS_ID = 'docker-hub-credentials'
        GOOGLE_JSON_CREDS_ID = 'google-svc-key' 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm [cite: 17]
            }
        }

        stage('Prepare Auth & Secrets') {
            steps {
                script {
                    // Saca o JSON do "cofre" do Jenkins e mete-o na pasta do backend para o Docker o copiar
                    withCredentials([file(credentialsId: "${GOOGLE_JSON_CREDS_ID}", variable: 'GOOGLE_JSON_FILE')]) {
                        sh "cp ${GOOGLE_JSON_FILE} ./backend/service-account.json"
                    }
                }
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    // Requisito: Enviar imagens para o Docker Hub 
                    docker.withRegistry('', "${DOCKER_CREDS_ID}") {
                        // O Dockerfile do backend deve fazer: COPY service-account.json .
                        def back = docker.build("${DOCKER_USER}/gym-backend:latest", "./backend")
                        back.push()
                        
                        def front = docker.build("${DOCKER_USER}/gym-frontend:latest", "./frontend")
                        front.push()
                    }
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                // Requisito: Aplicação deve ser instalada/atualizada via Ansible 
                echo "A executar Ansible Playbook..."
                // Certifica-te que criaste a pasta 'ansible' com o ficheiro 'playbook.yml'
                sh 'ansible-playbook ansible/playbook.yml'
            }
        }
    }

    post {
        always {
            script {
                // Requisito: Notificação por email em caso de sucesso ou erro 
                // Usando emailext para melhor suporte a STARTTLS/Gmail
                emailext (
                    to: 'sobreiraafonso@gmail.com',
                    subject: "Status Jenkins: ${currentBuild.fullDisplayName}",
                    body: "O build terminou com o resultado: ${currentBuild.result}\nVer detalhes em: ${env.BUILD_URL}"
                )
            }
        }
    }
}