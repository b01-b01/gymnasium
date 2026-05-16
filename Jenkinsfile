pipeline {
    agent any

    environment {
        DOCKER_USER = 'sobreiraa12344'
        // IDs das credenciais que deves ter no Jenkins (Manage Jenkins > Credentials)
        DOCKER_CREDS_ID = 'docker-credentials'
        GOOGLE_JSON_CREDS_ID = 'google-svc-key' 
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout simples sem sintaxe complexa para evitar erros de CPS
                checkout scm
            }
        }

        //stage('Prepare Secrets') {
        //    steps {
        //        script {
        //            // Saca o JSON do "cofre" do Jenkins e coloca-o na pasta para o Docker o copiar
        //            // Requisito: Segurança e gestão de ficheiros sensíveis [cite: 51]
        //            withCredentials([file(credentialsId: "${GOOGLE_JSON_CREDS_ID}", variable: 'GOOGLE_JSON_FILE')]) {
        //                sh "cp ${GOOGLE_JSON_FILE} ./backend/service-account.json"
        //            }
        //        }
        //    }
        //}

        stage('Docker Build & Push') {
            steps {
                script {
                    // Requisito: Containerização em múltiplas imagens (Front e Back) 
                    docker.withRegistry('', "${DOCKER_CREDS_ID}") {
                        
                        // Build e Push do Backend (Gymnasium API) 
                        def back = docker.build("${DOCKER_USER}/gym-backend:latest", "./backend")
                        back.push()
                        
                        // Build e Push do Frontend 
                        def front = docker.build("${DOCKER_USER}/gym-frontend:latest", "./frontend")
                        front.push()
                    }
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                // Esta sintaxe usa o plugin e evita o erro de "not found"
                ansiblePlaybook playbook: 'ansible/deploy.yml', inventory: 'ansible/inventory.ini'
            }
        }
    }

    post {
        always {
            // Requisito: Notificação por email em caso de sucesso ou erro 
            // Nota: Garante que configuraste o SMTP com a App Password de 16 dígitos
            mail to: 'sobreiraafonso@gmail.com',
                 subject: "Jenkins Build ${currentBuild.fullDisplayName}: ${currentBuild.result}",
                 body: "O pipeline do projeto Gymnasium terminou.\nResultado: ${currentBuild.result}\nURL: ${env.BUILD_URL}"
        }
    }
}