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

# README_LIST:
FULL-GUIDE: *GUIDE.MD*
Break-Down (part1): gke_deploy.info.md
Break-Down (part2): cloudSQL(postgres).setup.md

https://cloud.google.com/solutions/setting-up-cloud-sql-for-postgresql-for-production

# K8s: Kubectl CMDS:
*Imperitive*
kubectl create -f your-object-config.yaml
kubectl delete -f your-object-config.yaml
kubectl replace -f your-object-config.yaml
*Declarative*
kubectl diff -f configs/
kubectl apply -f configs/

# Cluster info:
kubectl get services

# To run locally, you need to open up 2-terminals:
docker build -t gcr.io/django-k8s-331621/polls:latest .

docker push gcr.io/django-k8s-331621/polls:latest

# one to run our Cloud-Proxy, and another to run ./manage.py runserver:
#
# CMD1:
# --- 
# ./cloud_sql_proxy -instances="django-k8s-331621:us-west1:k8s-1"=tcp:5432
# CMD2:
# ---
# ./manage.py runserver
