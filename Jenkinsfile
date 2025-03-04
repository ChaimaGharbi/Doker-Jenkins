pipeline {
    agent any

    triggers {
        githubPush()
    }
    
    environment {
        DOCKER_IMAGE = 'chaimagharbi/app'
        DOCKER_TAG = "${env.BUILD_NUMBER ?: 'latest'}"
        DOCKERHUB_CREDENTIALS = credentials('9f7142ad-0693-4e46-b021-9e4ed4ffe127')
    }

    stages {
        // stage('Test Docker Access') {
        //     steps {
        //         script {
        //             echo 'Running: Test Docker Access'
        //             sh 'sudo docker --version'
        //         }
        //     }
        // }

        stage('Checkout') {
            steps {
                echo 'Running: Checkout Repository'
                git branch: 'main',
                url: 'https://github.com/ChaimaGharbi/Doker-Jenkins.git'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Running: Setup Python Virtual Environment'
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
                echo 'Running: Lint & Static Analysis'
                sh '''
                    . venv/bin/activate
                    flake8 app/ --count --select=E9,F63,F7,F82
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running: Run Tests'
                sh '''
                    . venv/bin/activate
                    coverage run -m pytest app/tests/
                    coverage report --fail-under=80
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Running: Build Docker Image'
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running: Security Scan'
                sh "trivy image ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Running: Push to Docker Hub'
                script {
                    docker.withRegistry('https://index.docker.io/v1/', '9f7142ad-0693-4e46-b021-9e4ed4ffe127') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Running: Cleanup'
            script {
                node {
                    deleteDir()
                    sh 'docker logout || true'
                }
            }
        }
        
        success {
            echo 'Pipeline Succeeded: Deployment completed!'
        }
        
        failure {
            echo 'Pipeline Failed: Check the logs for errors.'
        }
    }
}
