pipeline {
    agent {
        kubernetes {
            label 'build'
            defaultContainer 'jnlp'
            idleMinutes 150
            activeDeadlineSeconds 300
            yaml libraryResource('pipeline/slave-template.yaml')
        }
    }
    environment {
        DOCKER_REGISTRY = "eu.gcr.io/example"
        APP_NAME = "hello-user"
        APP_VERSION = "${BRANCH_NAME}-${BUILD_NUMBER}"
    }
    options {
        disableConcurrentBuilds()
    }
    stages {
        stage('Build the image') {
            steps {
                sh "docker build -t ${DOCKER_REGISTRY}/${APP_NAME}:${APP_VERSION} ."
            }
        }
       // This step builds the image one more time
       // TODO: optimize the test environment setup
       stage ('Up Docker-Compose environment') {
            steps {
                sh "docker-compose up --build -d"
            }
        }
        stage('Test the image') {
            steps {
                sh "docker-compose exec -T api pytest"
            }
        }
        stage('Push the image') {
            steps {
                sh "docker push ${DOCKER_REGISTRY}/${APP_NAME}:${APP_VERSION}"
            }
        }
        stage('Trigger deploy to staging[head]') {
            when {
                branch 'master'
            }
            steps {
                build job: "/Deployments/${APP_NAME}/staging", wait: true, parameters: [
                    string(name: 'release', value: "${APP_VERSION}")
                ]
            }
        }
        stage('Trigger deploy to production') {
            when {
                branch 'master'
            }
            steps {
                script {
                    def proceed = true
                    try {
                        timeout(time: 1, unit: 'HOURS') {
                            input message: 'Deploy to production?'
                        }
                    } catch (err) {
                        proceed = false
                    }
                    if(proceed) {
                        // deployment steps
                        build job: "/Deployments/${APP_NAME}/production", wait: false, parameters: [
                            string(name: 'release', value: "${APP_VERSION}")
                        ]
                    }
                }
            }
        }
    }
    post {
        always {
            junit "tests/*.xml"
            sh "docker-compose down -v"
            deleteDir()
        }
        success {
            slackSend channel: '#jenkins-deploys', color: 'good',
                message: "${APP_NAME} build result ${APP_VERSION} (<${BUILD_URL}|Open>): SUCCESS"
        }
        failure {
            slackSend channel: '#jenkins-deploys', color: 'danger',
                message: "${APP_NAME} build result ${APP_VERSION} (<${BUILD_URL}|Open>): FAILURE"
        }
    }
}
