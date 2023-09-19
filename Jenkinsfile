pipeline{
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub'
        IMAGENAME = "axolotlite/pirl_api"
    }
    stages {
        stage('Build') {
            steps{
                script {
                    dockerImage = docker.build(IMAGENAME + ":$BUILD_NUMBER")
                }
            }
            post{
                success {
                    echo 'Image built successfully.'
                }
                failure {
                    echo "Image build failed."
                }
            }
        }
        stage('Push') {
            steps{
                script {
                    docker.withRegistry("", DOCKERHUB_CREDENTIALS ) {
                        dockerImage.push()
                    }
                }
            }
            post {
                success {
                    echo 'Image pushed successfully.'
                }
                failure {
                    echo "Image push failure."
                }
            }
        }

        stage('remove unused image') {
            steps{
                sh "docker rmi $IMAGENAME:$BUILD_NUMBER"
            }
        }
    }
}