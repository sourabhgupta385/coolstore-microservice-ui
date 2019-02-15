node{
    def NODEJS_HOME = tool "NODE_PATH"
    env.PATH="${env.PATH}:${NODEJS_HOME}/bin" 
   
    stage('First Time Deployment'){
        script{
            openshift.withCluster() {
                openshift.withProject("$APP_NAME-dev") {
                    def bcSelector = openshift.selector( "bc", "$MS_NAME")
                    def bcExists = bcSelector.exists()
                    if (!bcExists) {
                        openshift.newApp("$APP_TEMPLATE_URL")
                        sh 'sleep 190'
                    } else {
                        sh 'echo build config already exists in development'  
                    } 
                }
                openshift.withProject("$APP_NAME-test") {
                    def bcSelector = openshift.selector( "bc", "$MS_NAME")
                    def bcExists = bcSelector.exists()
                    if (!bcExists) {
                        openshift.newApp("$APP_NAME-dev/$MS_NAME:test")
                    } else {
                        sh 'echo build config already exists in QA'  
                    } 
                }
                openshift.withProject("$APP_NAME-prod") {
                    def bcSelector = openshift.selector( "bc", "$MS_NAME")
                    def bcExists = bcSelector.exists()
                    if (!bcExists) {
                        openshift.newApp("$APP_NAME-dev/$MS_NAME:test")
                    } else {
                        sh 'echo build config already exists in production'  
                    } 
                }
            }
        }
    }
    
    stage("Checkout Source"){
       checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: "$MS_SOURCE_URL"]]])
    }
    
    stage('Install Dependecies'){
        sh 'npm install'
    }
    
    stage('Code Quality'){
        sh 'npm run lint'
    }
   
    stage("Unit Test"){
         sh 'npm run test'
    }
    
    stage("Code Coverage"){
        sh 'npm run coverage'
    }

    stage("Dev - Building Application"){
        script{
            openshift.withCluster() {
                openshift.withProject("$APP_NAME-dev"){
                    openshift.startBuild("$MS_NAME")   
                }
            }
        }
    }
    
    stage("Tagging Image for Testing"){
        openshiftTag(namespace: '$APP_NAME-dev', srcStream: '$MS_NAME', srcTag: 'latest', destStream: '$MS_NAME', destTag: 'test')
    }
    
    stage("Tagging Image for Production"){
        openshiftTag(namespace: '$APP_NAME-dev', srcStream: '$MS_NAME', srcTag: 'latest', destStream: '$MS_NAME', destTag: 'prod')
    }
    
    stage("Test - Deploying Application"){
       openshiftDeploy(namespace:'$APP_NAME-test', deploymentConfig: '$MS_NAME')
    }
 
    stage("Functional Testing"){
        sh 'python functionalTest.py'
    }
   
    stage("Load Testing"){
        sh 'artillery run -o load.json perfTest.yml'
        sh 'artillery report load.json'
        
    }
    
    stage('Deploy to Production approval'){
        input "Deploy to prod?"
    }
    
    stage("Prod - Deploying Application"){
       openshiftDeploy(namespace:'$APP_NAME-prod', deploymentConfig: '$MS_NAME')
    }
    
    stage("Publishing Reports"){
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: '', reportFiles: 'quality.html', reportName: 'Quality Report', reportTitles: ''])
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'coverage', reportFiles: 'index.html', reportName: 'Code Coverage Report', reportTitles: ''])
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: '', reportFiles: 'load.json.html', reportName: 'Load Testing Report', reportTitles: ''])
        junit '**/results/test-results.xml'
    }
}
