# Set up Cloud SQL (Prev step @ /gke_deploy.info.md/#Setup Up CLoud SQL)
You need several **secrets** to enable your GKE(Google Kubernetes Engine) app to connect with your Cloud SQL instance (Postgres in this case). 
    One *secret* is required for instance-level access (connection), while the other two *secrets* are required for database access. 
        For more information about the two levels of access control, see Instance access control.
            - Instance Acces Control: https://cloud.google.com/sql/docs/mysql/instance-access-control
            - K8s Secrets: https://kubernetes.io/docs/concepts/configuration/secret/


To create the secret for instance-level access, provide the location ([PATH_TO_CREDENTIAL_FILE] ==> `./django-k8s-331621-91fe919253f2.json`) of the JSON service account key you downloaded when you created your service account (see Creating a service account in gke-deploy):
**Note: the path can be retrieved by right-click on the django-k8s-service file, navigate to "copy path"**
    e.g.
`kubectl create secret generic cloudsql-oauth-credentials   --from-file=credentials.json=//home/kcdouglass/Desktop/Cins465/cins465/DjangoCloud/Kubernetes-django-channels/django-k8s-331621-91fe919253f2.json`


# To create the secrets for database access (If wanted, one can create a Seperate SECRETS.yaml file for DB)
 use the Postgres database name, user name, and password defined in step 2 of Initializing your Cloud SQL instance (same as the one defined in mysite/settings.py):

 kubectl create secret generic cloudsql \
  --from-literal=database=DATABASE_NAME \
  --from-literal=username=DATABASE_USERNAME \
  --from-literal=password=DATABASE_PASSWORD

*e.g.*

DATABASE_NAME = `postgresk8s`
DATABASE_USERNAME = `django_user`
DATABASE_PASSWORD = `nach0pa$$`
kubectl create secret generic cloudsql \
  --from-literal=database=postgresk8s \
  --from-literal=username=django_user \
  --from-literal=password=nach0pa$$

-------
OUTPUT:
-------
secret/cloudsql created

# Next, Retrieve the public Docker image for the Cloud SQL proxy.

`docker pull gcr.io/cloudsql-docker/gce-proxy` ( :1.16 ) if wanted versioning
GCP wrong one: b.gcr.io/cloudsql-docker/gce-proxy

Build a Docker image, replacing <your-project-id> with your project ID.
docker build -t gcr.io/<your-project-id>/polls .
    e.g.
`docker build -t gcr.io/django-k8s-331621/polls .`

# Configure Docker to use gcloud as a credential helper, so that you can push the image to Container Registry:
gcloud auth configure-docker

# Push the Docker image. Replace <your-project-id> with your project ID.

docker push gcr.io/<your-project-id>/polls
`docker push gcr.io/django-k8s-331621/polls`

**Note: This command requires write access to Cloud Storage.** If you run this tutorial on a Compute Engine instance, your access to Cloud Storage might be read-only. To get write access, create a service account and use the service account to authenticate on your instance.


# Create the GKE resource:

kubectl create -f polls.yaml

**Note: If you used different names (other than cloudsql-oauth-credentials and cloudsql) when creating the secrets in the previous commands, then you need to update the polls.yaml file to match those new names.**

---
Output:
---
deployment.apps/polls created
service/polls created

# Deploy the app to GKE (Kubernetes Engine):
# Go To [GKE_Deply.info.md] for instructions