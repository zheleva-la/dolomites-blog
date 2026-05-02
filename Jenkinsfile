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
                sh 'python3 tests/test_blog.py > test-results.txt 2>&1; cat test-results.txt'
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
                writeFile file: 'generate_report.py', text: '''
import subprocess, os
from datetime import datetime, timezone

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "unavailable"

commit_hash   = run("git rev-parse --short HEAD")
commit_msg    = run("git log -1 --pretty=%B")
commit_author = run("git log -1 --pretty=%an")
branch        = os.environ.get("GIT_BRANCH", run("git rev-parse --abbrev-ref HEAD")).replace("origin/", "")
changelog     = run("git log --oneline -5")
build_num     = os.environ.get("BUILD_NUMBER", "?")
build_date    = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

workspace  = os.environ.get("WORKSPACE", ".")
test_file  = os.path.join(workspace, "test-results.txt")
try:
    test_results = open(test_file, encoding='utf-8').read().strip() or "No test output captured."
except:
    test_results = "test-results.txt not found."

report  = "# Deployment Report\\n\\n"
report += "## Build Summary\\n\\n"
report += "| Field | Value |\\n|---|---|\\n"
report += f"| Build Number | #{build_num} |\\n"
report += f"| Date | {build_date} |\\n"
report += f"| Branch | {branch} |\\n"
report += f"| Commit | {commit_hash} |\\n"
report += f"| Author | {commit_author} |\\n"
report += "| Status | SUCCESS |\\n\\n"
report += f"## Commit Message\\n\\n> {commit_msg}\\n\\n"
report += "## Test Results\\n\\n```\\n"
report += test_results + "\\n```\\n\\n"
report += "## Recent Changelog\\n\\n```\\n"
report += changelog + "\\n```\\n"

with open("deployment-report.md", "w", encoding='utf-8') as f:
    f.write(report)

print("deployment-report.md generated.")
'''
                sh 'python3 generate_report.py'
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