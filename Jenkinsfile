pipeline {
    agent any

    environment {
        PYTHON_PATH = "."
        // Project name for reporting
        PROJECT_NAME = "insider_project"
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
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m venv .venv
                            call .venv\\Scripts\\activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def runnerCmd = "python run_tests.py --headless --parallel"
                    
                    try {
                        if (isUnix()) {
                            sh ". .venv/bin/activate && ${runnerCmd}"
                        } else {
                            bat "call .venv\\Scripts\\activate && ${runnerCmd}"
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
            archiveArtifacts artifacts: 'reports/**/*.html, reports/**/*.png', fingerprint: true, allowEmptyArchive: true
            
            // Publish HTML report in Jenkins UI (requires HTML Publisher Plugin)
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
