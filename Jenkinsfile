pipeline {
    agent any

    environment {
        HEADLESS = "True"
        VENV_DIR = ".venv"
        REPORT_DIR = "reports"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                powershell '''
                    Write-Host "Creating virtual environment..."

                    python -m venv $env:VENV_DIR

                    Write-Host "Activating venv..."
                    & "$env:VENV_DIR\\Scripts\\Activate.ps1"

                    Write-Host "Upgrading pip..."
                    python -m pip install --upgrade pip

                    Write-Host "Installing dependencies..."
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Prepare Reports Folder') {
            steps {
                powershell '''
                    if (!(Test-Path $env:REPORT_DIR)) {
                        New-Item -ItemType Directory -Path $env:REPORT_DIR
                    }
                '''
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                    & "$env:VENV_DIR\\Scripts\\Activate.ps1"

                    Write-Host "Running pytest..."

                    pytest tests/test_qa_jobs.py `
                        --html="$env:REPORT_DIR\\report.html" `
                        --self-contained-html `
                        -v

                    exit 0
                '''
            }
        }
    }

    post {

        always {
            archiveArtifacts artifacts: 'reports/**/*.html, reports/**/*.png',
                fingerprint: true,
                allowEmptyArchive: true

            script {
                if (fileExists('reports/report.html')) {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'Selenium Test Report'
                    ])
                } else {
                    echo "Report not generated, skipping publishHTML."
                }
            }
        }

        success {
            echo 'Tests completed successfully!'
        }

        failure {
            echo 'Tests failed but artifacts are saved!'
        }
    }
}
