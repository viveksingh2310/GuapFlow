pipeline {
  agent any
  stages {
    stage("Verify Environment") {
      steps {
        bat "echo USER=%USERNAME%"
        bat "where python"
        bat "where py"
        bat "python --version"
        bat "py --version"
      }
    }
  }
}
