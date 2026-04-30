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
                bat '''
                    echo Creating virtual environment...
                    python -m venv %VENV_DIR%

                    echo Upgrading pip...
                    %VENV_DIR%\\Scripts\\python.exe -m pip install --upgrade pip

                    echo Installing dependencies...
                    %VENV_DIR%\\Scripts\\pip.exe install -r requirements.txt
                '''
            }
        }

        stage('Prepare Reports Folder') {
            steps {
                bat '''
                    if not exist %REPORT_DIR% mkdir %REPORT_DIR%
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    echo Running pytest...

                    %VENV_DIR%\\Scripts\\pytest.exe tests\\test_qa_jobs.py ^
                        --html=%REPORT_DIR%\\report.html ^
                        --self-contained-html ^
                        -v
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
