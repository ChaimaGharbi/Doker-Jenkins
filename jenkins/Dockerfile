FROM jenkins/jenkins:latest

USER root
RUN apt-get update \
      && apt-get install -y sudo \
      && apt install -y python3 python3-venv python3-pip \
      && rm -rf /var/lib/apt/lists/* 
      
RUN echo "jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers

USER jenkins
COPY plugins.txt /usr/share/jenkins/plugins.txt

# Install plugins using the jenkins-plugin-cli
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/plugins.txt
