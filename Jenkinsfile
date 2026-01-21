pipeline {
  agent any
  stages {
    stage("Verify Runtime") {
      steps {
        bat "whoami"
        bat "where python"
        bat "where py"
        bat "python --version"
        bat "py --version"
      }
    }
  }
}
