# Docker image
project name: `django-k8s`
project id: `django-k8s-331621`
<DOCKER_GCP_image> = `us.gcr.io/django-k8s-331621/django-k8s`

# Database
db instance-id: `k8s-1`
db-password: `nach0pa$$`
db name: `postgresk8s`
db user-name: `django_user`
db connection-name: `django-k8s-331621:us-west1:k8s-1`

CMD to create from local machine's CLI
gcloud sql databases create postgresk8s \
    --instance k8s-1