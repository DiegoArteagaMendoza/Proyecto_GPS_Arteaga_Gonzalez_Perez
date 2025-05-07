pipeline {
    agent any

    environment {
        IMAGE_NAME = 'diegoarteagamendoza2002/ms-inventario:1.0.2'
        DOCKERHUB_CREDENTIALS = 'dockerhub'
    }

    stages {
        stage('Clonar repositorio') {
            steps {
                git 'https://github.com/DiegoArteagaMendoza/Proyecto_GPS_Arteaga_Gonzalez_Perez.git'
            }
        }

        stage('Construir imagen Docker') {
            steps {
                script {
                    docker.build(IMAGE_NAME)
                }
            }
        }

        stage('Loguearse en DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image(IMAGE_NAME).push("latest")
                    }
                }
            }
        }

        stage('Desplegar en Docker Desktop') {
            steps {
                sh """
                    docker rm -f app || true
                    docker pull $IMAGE_NAME
                    docker run -d --name app -p 8081:80 $IMAGE_NAME
                """
            }
        }
    }
}
