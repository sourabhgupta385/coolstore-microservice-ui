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
                    } else {
                        sh 'echo build config already exists'  
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
    
    stage("Functional Testing"){
        sh 'python functionalTest.py'
    }
   
    stage("Load Testing"){
        sh 'artillery run perfTest.yml'
        
    }
    
    stage("Tagging Image for Production"){
        openshiftTag(namespace: '$APP_NAME-dev', srcStream: '$MS_NAME', srcTag: 'latest', destStream: '$MS_NAME', destTag: 'prod')
    }
    
    stage("Publishing Reports"){
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: '', reportFiles: 'quality.html', reportName: 'Quality Report', reportTitles: ''])
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'coverage', reportFiles: 'index.html', reportName: 'Code Coverage Report', reportTitles: ''])
        junit '**/results/test-results.xml'
    }
}
