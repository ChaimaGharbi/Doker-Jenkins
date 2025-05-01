FROM jenkins/jenkins:latest

USER root
# Install sudo, Python, pip, and Docker
RUN apt-get update \
    && apt-get install -y sudo \
    && apt install -y python3 python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://get.docker.com/ | sh \
    && usermod -aG docker jenkins  # Add jenkins user to docker group

# Install kubectl directly from Google's storage
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/

# Allow jenkins user to run sudo without a password prompt
RUN echo "jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers

USER jenkins

# Install Jenkins plugins
COPY plugins.txt /usr/share/jenkins/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/plugins.txt