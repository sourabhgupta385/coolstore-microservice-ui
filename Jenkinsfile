node{
    def NODEJS_HOME = tool "NODE_PATH"
    env.PATH="${env.PATH}:${NODEJS_HOME}/bin"
   
    stage('First Time Deployment'){
        script{
            openshift.withCluster() {
                openshift.withProject('coolstore-dev-sourabh') {
                    def bcSelector = openshift.selector( "bc", "web-ui")
                    def bcExists = bcSelector.exists()
                    if (!bcExists) {
                        openshift.newApp("https://raw.githubusercontent.com/sourabhgupta385/coolstore-microservice/stable-ocp-3.9/openshift/coolstore-template.yaml")
                    } else {
                        sh 'echo build config already exists'  
                    }
                }
            }
        }
    }
    
    stage('Install Dependecies'){
        sh 'npm --prefix ../workspace@script/coolstore-ui install'
    }
    
    stage('Code Quality'){
        sh 'npm --prefix ../workspace@script/coolstore-ui run lint'
        //publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: '', reportFiles: 'quality.html', reportName: 'Quality Report', reportTitles: ''])
        sh 'npm --prefix ../workspace@script/coolstore-ui run lint-console'
    }
    
    stage("Unit Test"){
        sh 'npm --prefix ../workspace@script/coolstore-ui run test'
    }
   
    stage("Code Coverage"){
        sh 'npm --prefix ../workspace@script/coolstore-ui run coverage'
    }

    stage("Dev - Building Application"){
        script{
            openshift.withCluster() {
                openshift.withProject('coolstore-dev-sourabh'){
                    openshift.startBuild("web-ui")   
                }
            }
        }
    }
    
    stage("Functional Testing"){
        sh 'cd ../workspace@script/coolstore-ui && python functionalTest.py'
        sh 'echo Function Testing' 
    }
   
    stage("Load Testing"){
        sh 'cd ../workspace@script/coolstore-ui && artillery run perfTest.yml'
        
    }
    
    stage("Tagging Image for Production"){
        openshiftTag(namespace: 'coolstore-dev-sourabh', srcStream: 'web-ui', srcTag: 'latest', destStream: 'web-ui', destTag: 'prod')
    }
}
