# Phonebook on App Engine

## Introduction
This application shows how to deploy an application to App Engine and integrate with other products such as Firestore, Redis and Cloud Armor.

## Deploy

### Terraform
1. Create a new project and select it
2. Open Cloud Shell, clone this repo into the Cloud Shell, then go to the folder
```
git clone https://github.com/sylvioneto/phonebook-appengine.git
cd ./phonebook-appengine
```
3. Ensure the var is set, otherwise set it with `gcloud config set project` command
```
echo $GOOGLE_CLOUD_PROJECT
```

4. Create a bucket to store your project's Terraform state
```
gsutil mb gs://$GOOGLE_CLOUD_PROJECT-tf-state
```

5. Enable the necessary APIs
```
gcloud services enable cloudbuild.googleapis.com redis.googleapis.com vpcaccess.googleapis.com \
compute.googleapis.com firestore.googleapis.com cloudresourcemanager.googleapis.com \
appengine.googleapis.com servicenetworking.googleapis.com
```

6. Go to [IAM](https://console.cloud.google.com/iam-admin/iam) and add `Editor` and `Service Networking Admin` roles to the Cloud Build's service account `<PROJECT_NUMBER>@cloudbuild.gserviceaccount.com`.

7. Execute Terraform using Cloud Build
```
gcloud builds submit ./terraform --config cloudbuild.yaml
```


### Application 

1. Create an app
```
gcloud app create --region=southamerica-east1
```

2. Go to [Create a Cloud Firestore](https://console.cloud.google.com/firestore/welcome) and make sure your database is in `Native` mode and in `southamerica-east1`.

3. Grant `Cloud Datastore User` role to `<PROJECT_ID>@appspot.gserviceaccount.com` service account.

3. Open the app.yaml file and update the `<REDIS_IP>` and `<PROJECT_ID>` values.

4. Install App Engine python dependencies
```
gcloud components install app-engine-python
```

5. Deploy the app:
```
cd ./app
gcloud app deploy --quiet
```

## Test
gcloud app browse

Testing
export FLASK_ENV=development; export FLASK_APP=main.py; python -m flask run
