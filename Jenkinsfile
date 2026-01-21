pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Verify Python") {
            steps {
                bat "py --version"
                bat "py -m pip --version"
            }
        }

        stage("Setup Python Environment") {
            steps {
                dir('backend') {
                    bat """
                    py -m venv venv
                    call venv\\Scripts\\activate.bat
                    py -m pip install --upgrade pip
                    pip install -r requirements.txt
                    """
                }
            }
        }

        stage("Inject Secrets") {
            steps {
                dir('backend') {
                    withCredentials([
                        file(credentialsId: 'user-service-env', variable: 'USER_ENV'),
                        file(credentialsId: 'loan-service-env', variable: 'LOAN_ENV'),
                        file(credentialsId: 'account-service-env', variable: 'ACCOUNT_ENV')
                    ]) {
                        bat """
                        copy %USER_ENV% user-service\\.env
                        copy %LOAN_ENV% loan-service\\.env
                        copy %ACCOUNT_ENV% account-service\\.env
                        """
                    }
                }
            }
        }

        stage("Run Tests") {
            steps {
                dir('backend') {
                    bat """
                    call venv\\Scripts\\activate.bat
                    pytest -v
                    """
                }
            }
        }
    }

    post {
        success {
            echo "CI Pipeline Successful using py ✅"
        }
        failure {
            echo "CI Pipeline Failed ❌"
        }
        always {
            cleanWs()
        }
    }
}
