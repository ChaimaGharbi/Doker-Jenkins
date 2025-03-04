pipeline {
    agent any

    triggers {
        githubPush()
    }
    
    environment {
        DOCKER_IMAGE = 'ChaimaGharbi/app'
        DOCKER_TAG = "${env.BUILD_NUMBER ?: 'latest'}"
        DOCKERHUB_CREDENTIALS = credentials('c9737c11-336f-4078-9eb8-838cc384f295')
    }

    
    stages {

        stage('Test Docker Access') {
            steps {
                script {
                    sh 'docker --version'
                }
            }
        }
      stage('Debug Jenkins Env') {
    steps {
        sh 'env | grep BUILD'
    }
}
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/ChaimaGharbi/Doker-Jenkins.git'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install pytest coverage flake8
                '''
            }
        }
        
        stage('Lint & Static Analysis') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 app/ --count --select=E9,F63,F7,F82
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    coverage run -m pytest app/tests/
                    coverage report --fail-under=80
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                // Assurez-vous que Trivy est installé
                sh "trivy image ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Utilisez l'ID de credentials correct
                    docker.withRegistry('https://index.docker.io/v1/', 'c9737c11-336f-4078-9eb8-838cc384f295') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
    
    post {
        always {
          script {
          node {
            
                deleteDir()
                sh 'docker logout || true'
            }
          }
        }
        
        success {
            echo 'Déploiement réussi !'
        }
        
        failure {
            echo 'Échec du pipeline'
        }
    }
}