# Sample Openshift CI/CD pipeline for Node + AngularJS microservice

## Manual Deployment Instructions

### 1. Create Lifecycle Stages

For the purposes of this demo, we are going to create two stages for our application to be promoted through.

- `coolstore-ui-cicd`
- `coolstore-ui-dev`

```
$ oc new-project coolstore-ui-cicd
$ oc new-project coolstore-ui-dev
```

### 2. Stand up Jenkins master in coolstore-ui-cicd

For this step, the OpenShift default template set provides exactly what we need to get jenkins up and running.

Deploy jenkins-persistent template from the catalog in OpenShift.

### 3. Add permissions for jenkins to make changes in coolstore-ui-dev project

```
$ oc policy add-role-to-user admin system:serviceaccount:coolstore-ui-cicd:jenkins -n coolstore-ui-dev
$ oc policy add-role-to-user edit system:serviceaccount:coolstore-ui-cicd:jenkins -n coolstore-ui-dev
```

### 4. Instantiate Pipeline

A _pipelineTemplate_ is provided that defines pipeline buildConfig. And _parameters.txt_ defines all the parameters.

```
$ oc process -f pipelineTemplate.yaml --param-file=parameters.txt | oc create -f - -n coolstore-ui-cicd
```

### 5. Start Pipeline

```
$ oc start-build coolstore-ui-pipeline -n coolstore-ui-cicd
```
