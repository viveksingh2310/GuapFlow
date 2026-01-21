pipeline {
    agent any
    environment {
        PYTHON = "python"
        VENV = "venv"
    }
    stages {
        stage("Checkout") {
            steps {
                checkout scm
            }
        }
        stage("Setup Python Environment") {
            steps {
                dir('backend') {
                    bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
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
                        bat '''
                        copy %USER_ENV% user-service\\.env
                        copy %LOAN_ENV% loan-service\\.env
                        copy %ACCOUNT_ENV% account-service\\.env
                        '''
                    }
                }
            }
        }
        stage("Run Tests") {
            steps {
                dir('backend') {
                    bat '''
                    call venv\\Scripts\\activate
                    pytest tests -v
                    '''
                }
            }
        }
        stage("Service-Level Tests") {
            steps {
                dir('backend') {
                    bat '''
                    call venv\\Scripts\\activate
                    pytest user-service
                    pytest loan-service
                    pytest account-service
                    '''
                }
            }
        }
    }
    post {
        success {
            echo "CI Pipeline Successful on Windows ✅"
        }
        failure {
            echo "CI Pipeline Failed ❌"
        }
        always {
            cleanWs()
        }
    }
}
