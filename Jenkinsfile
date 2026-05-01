pipeline {
    agent any

    environment {
        DEPLOY_DIR = '/var/www/honeymoon-blog'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'python3 tests/test_blog.py'
            }
        }

        stage('Build') {
            steps {
                echo 'Building site...'
                sh '''
                    mkdir -p dist
                    cp -r src/* dist/
                    echo "Build complete: $(date)" > dist/build.txt
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to web server...'
                sh '''
                    mkdir -p ${DEPLOY_DIR}
                    cp -r dist/* ${DEPLOY_DIR}/
                    echo "Deployed successfully at $(date)"
                '''
            }
        }

    }

    post {
        success {
            echo 'Pipeline succeeded! Your honeymoon blog is live.'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
    }
}
