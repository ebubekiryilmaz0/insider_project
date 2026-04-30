pipeline {
    agent any

    environment {
        PYTHON_PATH = "."
        PROJECT_NAME = "insider_project"
        VENV_DIR = ".venv"
        REPORT_DIR = "reports"
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                            python3 -m venv ${VENV_DIR}
                            . ${VENV_DIR}/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        """
                    } else {
                        bat """
                            python -m venv ${VENV_DIR}
                            call ${VENV_DIR}\\Scripts\\activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        """
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Use our robust terminal runner
                    def runnerCmd = "python run_tests.py --headless --parallel"
                    
                    try {
                        if (isUnix()) {
                            sh ". ${VENV_DIR}/bin/activate && ${runnerCmd}"
                        } else {
                            bat "call ${VENV_DIR}\\Scripts\\activate && ${runnerCmd}"
                        }
                    } catch (exc) {
                        currentBuild.result = 'UNSTABLE'
                        echo "Tests failed, but continuing to archive reports."
                    }
                }
            }
        }
    }

    post {
        always {
            // Archive the HTML report and screenshots
            archiveArtifacts artifacts: "${REPORT_DIR}/**/*.html, ${REPORT_DIR}/**/*.png", 
                             fingerprint: true, 
                             allowEmptyArchive: true
            
            script {
                if (fileExists("${REPORT_DIR}/report.html")) {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: "${REPORT_DIR}",
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
