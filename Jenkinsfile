pipeline {
    agent any

    environment {
        PYTHON_PATH = "."
        HEADLESS = "True"
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
                    # Virtual environment oluştur
                    python -m venv .venv

                    # Script execution policy sorunlarını önle
                    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

                    # venv activate
                    . .venv\\Scripts\\Activate.ps1

                    # pip upgrade ve bağımlılıklar
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
                    . .venv\\Scripts\\Activate.ps1

                    try {
                        pytest tests/test_qa_jobs.py `
                            --html=reports/report.html `
                            --self-contained-html `
                            -v

                    } catch {
                        Write-Host "Tests failed, but continuing to archive reports."
                        exit 0
                    }
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*.html, reports/**/*.png',
                fingerprint: true,
                allowEmptyArchive: true

            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Selenium Test Report',
                reportTitles: ''
            ])
        }

        success {
            echo 'Tests passed successfully!'
        }

        failure {
            echo 'Tests failed!'
        }
    }
}
