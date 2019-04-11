pipeline {
    options {
        buildDiscarder(logRotator(numToKeepStr: '2', artifactNumToKeepStr: '2'))
    }
    environment {
        DOCKER = credentials('docker')
    }
    agent any
        stages {
            stage('PreBuild') {
                steps {
                    sh 'python3 -m virtualenv venv'
                    sh 'chmod a+x venv/bin/activate'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                    sh '. venv/bin/activate && pip install codecov pytest pytest-cov mock'
                }
            }
            stage('Build') {
                steps {
                    sh '. venv/bin/activate && make build'
                }
                post {
                    success {
                        echo 'Build succeeded.'
                    }
                    failure {
                        echo 'Build failed.'
                    }
                }
            }
            stage('Test') {
                steps {
                    sh '. venv/bin/activate && make test'
                }
                post {
                    success {
                        sh '. venv/bin/activate && python3 -m codecov --token f87444f1-1c2d-4f8d-9f54-14089c09c18c'
                    }
                }
            }
            stage('Deploy') {
                when {
                    branch 'master'
                }
                steps {
                    echo 'This is the Deploy Stage'
                }
                post {
                    success {
                        sh 'docker login -u "$DOCKER_USR" -p "$DOCKER_PSW" && docker build -t "$DOCKER_USR"/crowdsourcedev:latest . '
                        sh 'Image="$(docker images | grep "crowdsourcedev" | head -1 | grep -v grep | awk \'{print $3}\')" && docker tag $Image "$DOCKER_USR"/crowdsourcedev:latest && docker push "$DOCKER_USR"/crowdsourcedev'
                    }
                    failure {
                        echo 'Deploy failed'
                    }
                }
            }
            stage('Cleanup') {
                steps {
                    sh 'make clean'
                }
            }
        }
    }
