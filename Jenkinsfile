pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Preparar entorno') {
            steps {
                sh 'test -f .env || cp .env.example .env'
            }
        }

        stage('Pruebas') {
            steps {
                sh 'python3 -m pip install --user pytest'
                sh 'python3 -m pytest'
            }
        }

        stage('Construir imagenes') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Probar comunicacion') {
            steps {
                sh 'docker compose up -d --wait'
                sh 'python3 jenkins/probar_comunicacion.py'
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v || true'
        }
    }
}
