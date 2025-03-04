pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE = 'chaimagharbi/app'
        DOCKER_TAG = "${env.BUILD_NUMBER ?: 'latest'}"
    }

    stages {
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
                    sh 'sudo docker build -t "${DOCKER_IMAGE}:${DOCKER_TAG}" .'
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Running: Push to Docker Hub'
                script {
                    withCredentials([usernamePassword(credentialsId: '71f95ee8-3d30-4471-bba3-5f3d0a970b3d', 
                        usernameVariable: 'DOCKER_USER', 
                        passwordVariable: 'DOCKER_PASS')]) {

                        sh 'echo "$DOCKER_PASS" | sudo docker login -u "$DOCKER_USER" --password-stdin'

                        docker.withRegistry('https://index.docker.io/v1/', '71f95ee8-3d30-4471-bba3-5f3d0a970b3d') {
                            dockerImage.push()
                            dockerImage.push('latest')
                        }
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
                    sh 'sudo docker logout || true'
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
