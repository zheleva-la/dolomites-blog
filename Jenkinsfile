pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

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
                    python3 - <<PYEOF
import subprocess, os
from datetime import datetime, timezone

def run(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()

commit_hash  = run("git rev-parse --short HEAD")
commit_msg   = run("git log -1 --pretty=%B")
commit_author = run("git log -1 --pretty=%an")
branch       = os.environ.get("GIT_BRANCH", run("git rev-parse --abbrev-ref HEAD")).replace("origin/", "")
changelog    = run("git log --oneline -5 || echo 'No changelog available'")
build_num    = os.environ.get("BUILD_NUMBER", "?")
build_date   = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

workspace    = os.environ.get("WORKSPACE", ".")
test_file    = os.path.join(workspace, "test-results.txt")
try:
    test_results = open(test_file).read().strip() or "No test output captured."
except:
    test_results = "test-results.txt not found."

report = f"""# Deployment Report

## Build Summary

| Field        | Value |
|-------------|-------|
| Build Number | #{build_num} |
| Date         | {build_date} |
| Branch       | {branch} |
| Commit       | {commit_hash} |
| Author       | {commit_author} |
| Status       | SUCCESS |

## Commit Message

> {commit_msg}

## Test Results

```
{test_results}
```

## Recent Changelog

```
{changelog}
```
"""

with open("deployment-report.md", "w") as f:
    f.write(report)

print("deployment-report.md generated.")
PYEOF
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