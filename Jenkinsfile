pipeline {

  agent any

  stages {
    
    stage("Pull Image") {

      steps {
        echo 'Descagando la imagen'

        script {
          docker.withRegistry('https://registry.hub.docker.com', 'duckerhub-creds') {
            docker.image('diegoarteagamendoza2002/ms-inventario:1.0.2').pull()
          }
        }
      }
    }

  }
}
