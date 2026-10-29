pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Verify Project') {
            steps {
                sh '''
                    set -e

                    echo "Checking Flask backend..."
                    test -f backend/app.py
                    test -f backend/requirements.txt

                    echo "Checking Express frontend..."
                    test -f frontend/server.js
                    test -f frontend/package.json

                    echo "Project structure verified successfully."
                '''
            }
        }

        stage('Check Runtime Versions') {
            steps {
                sh '''
                    python3 --version
                    node --version
                    npm --version
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
