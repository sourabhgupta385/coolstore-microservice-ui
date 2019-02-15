# Sample Openshift CI/CD pipeline for Node + AngularJS microservice

## Manual Deployment Instructions

### 1. Create Lifecycle Stages

For the purposes of this demo, we are going to create two stages for our application to be promoted through.

- `coolstore-ui-cicd`
- `coolstore-ui-dev`
- `coolstore-ui-test`
- `coolstore-ui-prod`

```
$ oc new-project coolstore-ui-cicd
$ oc new-project coolstore-ui-dev
$ oc new-project coolstore-ui-test
$ oc new-project coolstore-ui-prod
```

### 2. Stand up Jenkins master in coolstore-ui-cicd

For this step, the OpenShift default template set provides exactly what we need to get jenkins up and running.

Deploy jenkins-persistent template from the catalog in OpenShift.

### 3. Add permissions for jenkins to make changes in dev, test and prod project

```
$ oc policy add-role-to-user admin system:serviceaccount:coolstore-ui-cicd:jenkins -n coolstore-ui-dev
$ oc policy add-role-to-user edit system:serviceaccount:coolstore-ui-cicd:jenkins -n coolstore-ui-dev

$ oc policy add-role-to-user admin system:serviceaccount:coolstore-ui-cicd:jenkins -n coolstore-ui-test
$ oc policy add-role-to-user edit system:serviceaccount:coolstore-ui-cicd:jenkins -n coolstore-ui-test

$ oc policy add-role-to-user admin system:serviceaccount:coolstore-ui-cicd:jenkins -n coolstore-ui-prod
$ oc policy add-role-to-user edit system:serviceaccount:coolstore-ui-cicd:jenkins -n coolstore-ui-prod
```
### 4. Add permissions for test and prod project to pull images from dev project

```
$ oc policy add-role-to-group system:image-puller system:serviceaccounts:coolstore-ui-test -n coolstore-ui-dev
$ oc policy add-role-to-group system:image-puller system:serviceaccounts:coolstore-ui-prod -n coolstore-ui-dev
```

### 5. Instantiate Pipeline

A _pipelineTemplate_ is provided that defines pipeline buildConfig. And _parameters.txt_ defines all the parameters.

```
$ oc process -f pipelineTemplate.yaml --param-file=parameters.txt | oc create -f - -n coolstore-ui-cicd
```

### 6. Start Pipeline

```
$ oc start-build coolstore-ui-pipeline -n coolstore-ui-cicd
```
