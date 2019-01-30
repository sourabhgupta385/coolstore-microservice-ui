node{
    def NODEJS_HOME = tool "NODE_PATH"
    env.PATH="${env.PATH}:${NODEJS_HOME}/bin" 
   
    stage('First Time Deployment'){
        script{
            openshift.withCluster() {
                openshift.withProject("$APP_NAME-dev") {
                    sh "echo $APP_TEMPLATE_URL"
                    def bcSelector = openshift.selector( "bc", "web-ui")
                    def bcExists = bcSelector.exists()
                    if (!bcExists) {
                        openshift.newApp("$APP_TEMPLATE_URL")
                    } else {
                        sh 'echo build config already exists'  
                    } 
                }
            }
        }
    }
    
    stage("Checkout Source"){
       checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/sourabhgupta385/coolstore-microservice-ui.git']]])
    }
    
    stage('Install Dependecies'){
        sh 'npm install'
    }
    
    stage('Code Quality'){
        sh 'npm run lint'
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: '', reportFiles: 'quality.html', reportName: 'Quality Report', reportTitles: ''])
        sh 'npm run lint-console'
    }
    
    stage("Unit Test"){
        sh 'npm run test'
        sh 'npm run test-jenkins'
    }
   
    stage("Code Coverage"){
        sh 'npm run coverage'
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './results/', reportFiles: 'test-results.xml', reportName: 'Test Report', reportTitles: ''])
    }

    stage("Dev - Building Application"){
        script{
            openshift.withCluster() {
                openshift.withProject("$APP_NAME-dev"){
                    openshift.startBuild("web-ui")   
                }
            }
        }
    }
    
    stage("Functional Testing"){
        sh 'python functionalTest.py'
    }
   
    stage("Load Testing"){
        sh 'artillery run perfTest.yml'
        
    }
    
    stage("Tagging Image for Production"){
        openshiftTag(namespace: '$APP_NAME-dev', srcStream: 'web-ui', srcTag: 'latest', destStream: 'web-ui', destTag: 'prod')
    }
    
    post {
      always {
        junit '**/reports/test-results.xml'
      }
   }
}
