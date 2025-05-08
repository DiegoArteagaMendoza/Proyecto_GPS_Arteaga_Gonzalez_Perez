pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-user')  // ID que configuraste
    }

    stages {
        stage('Desplegar contenedor') {
            steps {
                sh 'echo "$DOCKERHUB_CREDENTIALS_USR"'
                sh 'docker login -u "$DOCKERHUB_CREDENTIALS_USR" -p "$DOCKERHUB_CREDENTIALS_PSW"'
                sh 'docker pull diegoarteagamendoza2002/ms-inventario:latest'
                sh 'docker stop app || true && docker rm app || true'
                sh 'docker run -d --name app -p 80:80 tu_usuario/tu_imagen:latest'
            }
        }
    }
}
