pipeline {
    agent any

    environment {
        IMAGE_NAME = "diegoarteagamendoza2002/ms-inventario"
        IMAGE_TAG = "1.0.2"
        CONTAINER_NAME = "ms-inventario"
    }

    stages {
        stage('Descargar imagen desde DockerHub') {
            steps {
                script {
                    sh "docker pull ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Detener contenedor anterior') {
            steps {
                script {
                    // Detener y eliminar el contenedor si ya existe
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Levantar nuevo contenedor') {
            steps {
                script {
                    // Ejecutar el contenedor con la nueva imagen
                    sh "docker run -d --name ${CONTAINER_NAME} -p 8080:8080 ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
}
