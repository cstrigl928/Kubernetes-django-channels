After you make updates to your project, you need to:
    (1) Rebuild the DOcker image:
    (2) to check if it works locally still
    (3) Configure Docker to use Gcloud as a Credential Helper, so that we can push the image to Container Registry
    (4) Push to GKE registry

    **Commands in that order**
    <DOCKER_IMAGE> = gcr.io/django-k8s-331621/polls
      
    docker build -t gcr.io/django-k8s-331621/polls .
    # -----
# To run locally, you need to open up 2-terminals:
# one to run our Cloud-Proxy, and another to run ./manage.py runserver:
#
# CMD1:
# --- 
# ./cloud_sql_proxy -instances="django-k8s-331621:us-west1:k8s-1"=tcp:5432
# CMD2:
# ---
    <!-- docker run -p 80:80 gcr.io/django-k8s-331621/polls -->
# ./manage.py runserver
    gcloud auth configure-docker
    docker push gcr.io/django-k8s-331621/polls
    kubectl describe pods
    <!-- kubectl set image deployments/polls To :Latest -->
    kubectl get pods   # Should show recent update
    kubectl describe services/polls # show cluster information, labels, IP-Address, LoadBalancers Ingress

    # if you've update any Resource packages (YAML), then also update them as well:

    kubectl apply -f polls.yaml

    * If you've only just created a NEW resource (e.g. Added resource for Redis) then you need to use the 'create' command with kubectl: *

        kubectl create -f redis.yaml
        --OUT--
        deployment "redis" created
        service "redis" created

        - After the resources are UPDATED, there should be three polls pods on the cluster. Check the status of the pods:

            kubectl get pods
            kubectl logs <your-pod-id>
            kubectl cluster-info
    
    
    
    
    CMD to create from local machine's CLI
gcloud sql databases create postgresk8s \
    --instance k8s-1