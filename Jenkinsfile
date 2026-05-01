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
                sh 'python3 tests/test_blog.py 2>&1 | tee test-results.txt'
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

        stage('Docs') {
            steps {
                echo 'Generating deployment report...'
                sh '''
                    COMMIT_HASH=$(git rev-parse --short HEAD)
                    COMMIT_MSG=$(git log -1 --pretty=%B)
                    COMMIT_AUTHOR=$(git log -1 --pretty=%an)
                    BRANCH=$(git rev-parse --abbrev-ref HEAD)
                    BUILD_DATE=$(date "+%Y-%m-%d %H:%M:%S UTC")
                    CHANGELOG=$(git log --oneline -5)

                    cat > deployment-report.md << EOF
# Deployment Report

## Build Summary

| Field        | Value                        |
|-------------|------------------------------|
| Build Number | #${BUILD_NUMBER}            |
| Date         | ${BUILD_DATE}               |
| Branch       | ${BRANCH}                   |
| Commit       | ${COMMIT_HASH}              |
| Author       | ${COMMIT_AUTHOR}            |
| Status       | SUCCESS                     |

## Commit Message

> ${COMMIT_MSG}

## Test Results

\`\`\`
$(cat test-results.txt)
\`\`\`

## Recent Changelog

\`\`\`
${CHANGELOG}
\`\`\`
EOF
                '''
            }
        }

    }

    post {
        always {
            archiveArtifacts artifacts: 'deployment-report.md', fingerprint: true
        }
        success {
            echo 'Pipeline succeeded! Your honeymoon blog is live.'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
    }
}