pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE = 'chaimagharbi/app'
        DOCKER_TAG = "${env.BUILD_NUMBER ?: 'latest'}"
        DOCKER_CREDENTIALS_ID = '61caa30f-a4ab-4359-a067-0632a5007754'
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
                    dockerImage = sh(script: 'sudo docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest .', returnStdout: true).trim()
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Running: Push to Docker Hub'
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo "$DOCKER_PASS" | sudo docker login -u "$DOCKER_USER" --password-stdin'
                        docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                            sh "sudo docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                            sh "sudo docker push ${DOCKER_IMAGE}:latest"
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
            echo 'Pipeline Failed: Check the logs for errors..'
        }
    }
}
