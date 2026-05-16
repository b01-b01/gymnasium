FROM jenkins/jenkins:lts

USER root

# Atualiza o sistema e instala o Docker CLI + Ansible automaticamente
RUN apt-get update && \
    apt-get install -y docker.io ansible && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Adiciona o utilizador jenkins ao grupo do docker para poder correr comandos docker
RUN usermod -aG docker jenkins

USER jenkins