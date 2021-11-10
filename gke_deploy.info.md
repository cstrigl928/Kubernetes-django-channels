# Deploy the app to GKE (Google Kubernetes Engine)
When the app is deployed to Google Cloud, it uses the Gunicorn server. Gunicorn doesn't serve static content, so the app uses Cloud Storage to serve static content.

Collect and upload static resources
Create a Cloud Storage bucket and make it publicly readable.

gsutil mb gs://django-k8s-331621_gameroom-static
gsutil defacl set public-read gs://django-k8s-331621_gameroom-static

Gather all the static content locally into one folder:


python manage.py collectstatic
Upload the static content to Cloud Storage:


gsutil -m rsync -r ./static gs://django-k8s-331621_gameroom-static/static

In mysite/settings.py, set the value of STATIC_URL to the following URL, replacing [YOUR_GCS_BUCKET] with your bucket name:

gcloud container clusters create polls \
  --scopes "https://www.googleapis.com/auth/userinfo.email","cloud-platform" \
  --num-nodes 4 --zone "us-central1-a"

 --machine-type "e2-micro" --image-type "COS"
--scopes "https://www.googleapis.com/auth/userinfo.email","cloud-platform" \
  --num-nodes 3 --zone "us-west1-b"

http://storage.googleapis.com/django-k8s-331621_gameroom



(3) After the cluster is created, use the kubectl command-line tool, which is integrated with the gcloud, to interact with your GKE cluster. Because gcloud and kubectl are separate tools, make sure kubectl is configured to interact with the right cluster.

gcloud container clusters get-credentials polls --zone "us-west1-b"
------
OUTPUT: 
------
Fetching cluster endpoint and auth data.
kubeconfig entry generated for polls.

---
Make sure you see the Node:
---
kubectl get nodes (should say 'running')

# Set up Cloud SQL (Go to [cloudSql(postgres).setup.md] for instructions)
-- instructions modularlized for easier reading.

-----------------------------

# Deploy the app to GKE (Kubernetes Engine):
# FROM [GKE_Deply.info.md] for previous instructions

After the resources are created, there are three polls pods on the cluster. Check the status of your pods:

kubectl get pods
---
OUTPUT:
---
NAME                    READY   STATUS    RESTARTS   AGE
polls-7f5986955-4clsm   2/2     Running   0          3m47s
polls-7f5986955-rc2xs   2/2     Running   0          3m47s
polls-7f5986955-txvtx   2/2     Running   0          3m47s


**Wait a few minutes for the pod statuses to display as Running**. If the pods aren't ready or if you see restarts, you can get the logs for a particular pod to figure out the issue. [YOUR-POD-ID] is a part of the output returned by the previous kubectl get pods command.

kubectl logs [YOUR_POD_ID]

kubectl get pods -o wide

# See the app run in Google Cloud
After pods are "Ready" you can get the public IP address of the 
<load balancer/>
kubectl get services polls

**Note the EXTERNAL-IP address**, and go to http://[EXTERNAL-IP] in your browser to see the Django polls landing page and access the admin console

http://35.230.93.46 Will now show our Django Application on Kubernetes Engine hosted in Google Cloud, with Gs-util serving static and Postgres Database.