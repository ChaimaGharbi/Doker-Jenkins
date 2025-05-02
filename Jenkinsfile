pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE = 'chaimagharbi/app'
        DOCKER_TAG = "${env.BUILD_NUMBER ?: 'latest'}"
        DOCKER_CREDENTIALS_ID = 'd0dac775-94d4-4ddd-8dc3-fdc7d766b7d7'
        HELM_CHART_PATH = './mon-app'
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
                    dockerImage = docker.build(
                        "${DOCKER_IMAGE}",
                        "--tag ${DOCKER_IMAGE}:${DOCKER_TAG} --tag ${DOCKER_IMAGE}:latest ."
                    )
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Running: Push to Docker Hub'
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        dockerImage.push("${DOCKER_TAG}")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy with Helm') {
            steps {
                script {
                    sh 'helm upgrade --install mon-app $HELM_CHART_PATH'
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
