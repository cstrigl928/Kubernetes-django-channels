# Deploy Django web app to Google K8s
(1) Start Django Project or Clone the Official Django Polls App.
    Clone:
    ------
        git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    Start Fresh:
    ------
        `django-admin startproject <mysite>`
        cd <mysite>
        mkdir templates
        mkdir static
        `python manage.py startapp <app1>`    -- Don't forget to add <app1> to your installed_apps 
        mkdir templates/<app1>
        touch templates/<app1>/index.html
        mkdir static/<app1>
        mkdir static/<app1>/style.css
        -- in <mysite>/settings.py, create routes for TEMPLATE_DIRS and STATICFILES_DIRS, as os.path.join(BASE_DIR, 'templates') and os.path.join(BASE_DIR, 'static'), respecitivly
        *check that it runs* 
        `./manage.py runserver`

*Important Note!*
----------------
I am using virtual environment in this setup, if do not wish to just make sure that your Python version is greter that 3.7.3 or higher.

        `python -m venv venv`
        `source venv/bin/activate`
        `pip install --upgrade pip`
        `pip install -r requirements.txt`

(2) Open Existing or Create New Project on Google Cloud account.
# (3) Create Cloud Auth Proxy
*Since we want to store chat messages and have data persist from our database (models.py) accross multiple clusters, we need one unified database. This is where Google Cloud SQl comes in.* 
-   Google Cloud SQL allows you to choose between a few types of Relational databases (SQL, POSTGRES, ..) however here we will be using Postgres so you can see how easy it is to swap out the default Django Sqlite3 Object relational Mapper (ORM). Cloud SQL allows you to configure a DBMS such that you can provision usage, scale instances by way of automation, change storage capacity and handle other time consuming tasks in minutes which would otherwise take much longer.

    # Configure Cloud SQL to work in Development and when Deployed on K8s Via Cloud SQL Auth Proxy:
    -   Cloud SQL Auth Proxy provides secure access to your instances without the need for authorized networkds or configuring SSL certification. To learn more about how Cloud SQL Auth Proxy visit official google documentation here: <link="https://cloud.google.com/sql/docs/postgres/sql-proxy"/> .

    -   When configuring our Cloud SQL instance we need to remember to configure for both Local developement and K8s Deployment.
    When Deployed, we want our Django web app to use the Cloud SQL AUth Proxy that is built into the Google Kubernetes Engine environment such that it communicates with our Cloud SQL (Postgres) instance. To do so, we need to authenticate on our local computer (im using ubuntu) and obtain credentials from gcloud for the API:
        `gcloud auth application-default login`
    *this will open a browser tab and prompt you to login to your gcloud account. Once you've signed it leave this window open to keep the connection, if you close it you will lose connection. However we will not be using this tab anymore.*

    -   Download the Cloud SQL Auth Proxy (linux 64-bit):
        `wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy`
    -   Make the Proxy an executable via chmod +x command (change-mode) in your terminal:
        `chmod +x cloud_sql_proxy`

    **Note: Accoring to Google CLoud, "You can choose to move the download to somewhere common, such as a location on your PATH, or your home directory. If you choose to do this, when you start the Cloud SQL Auth proxy later on in the tutorial, remember to reference your chosen location when using cloud_sql_proxy commands."**

# (4) Settup Backend Services 
* Postgres, GS-Util for serving static content.
    * Create Postgres Instance
        Django supports relational databases out of the box but because Django offers support for Postgres and Googles Cloud SQL offers support for Postgres, that is what we are going to use. Also, I would be doing you a diservice if I did not tell you that you could also have multiple relational databases configured in your django project. Although we will not be doing that here, I want to throw that little peice of gold nugget out for those interested. To give a brief description of what needs to be done, you would simply go to your <mysite>/settings.py where 
        DATABASES = [
            ...
        ]  
        is defined. Note how it is a list of Dictionaries such that each dictionary key refers to a Database... 

        Ok ok.. Let's get back on track!
        2-ways to create a Postgres instance, one is through the Google cloud UI and the other is with the command line. I suggest using the UI so you get accustomed to the vast amount of options you have when configuring your DBMS <link="https://console.cloud.google.com/sql/instances?_ga=2.53323496.1148220492.1636612663-1560281031.1634941120&_gac=1.150684100.1634974855.CjwKCAjwwsmLBhACEiwANq-tXKEARSvBE_6hw5H61r35YO259FO4o025i6bwFpgddaj82kAzTqUNRxoCqRUQAvD_BwE">.
        
        If you simply wish to "just get it working" here is the command(s) that Google provides for setting up via your local command line (GET YOUR INFO FROM YOUR GCP DASHBOARD):
        - To get your Project ID via command line: `gcloud config get-value project`
        - For more info, : `gcloud config list`
        
        `gcloud sql instances create **INSTANCE_NAME** \`
            `--project **PROJECT_ID** \`
            `--database-version POSTGRES_13 \`
            `--tier db-f1-micro \`
            `--region **REGION**`

        ## And, REPLACE the following!

        **INSTANCE_NAME:** the Cloud SQL instance name
        **PROJECT_ID**: the Google Cloud project ID
        **REGION**: the Google Cloud region

        *It takes a few minutes to create the instance and for it to be ready for use.*

        Now, that our instance is created in GCP, let's create the actual database:
        `gcloud sql databases create *DATABASE_NAME* --instance *INSTANCE_NAME*`
        where *DATABASE_NAME* is whatever you want it to be, and *INSTANCE_NAME* matches the Cloud SQL instance you created in the previous step directly before this.


        # Tip: If you havn't already, you should create a file in your <mysite> directory that contains information pertaining to your GCP instance groups we're creating. Although it can be easily accessible through gcloud API, it comes in handy down the road when we go to make connections in our Kubernetes Deployment and Service YamL files. I ussually create a file gke_project_info.md and include:
             *Project:
             project_name: MyProject_Name (Google Cloud main project name) 
             project_id: my_Project_id,  
             DOCKER_GCP_image> = MY_DOCKER_IMAGE (not yet obtained),
                for example, mine were:
                    project name: `django-k8s`
                    project id: `django-k8s-331621`
                    <DOCKER_GCP_image> = `us.gcr.io/django-k8s-331/django-k8s`
            *Database*
             DB-name, 
             DB-ID, 
             DB-USERNAME, 
             DB-PASSWORD, and 
             DB-CONNECTION-NAME (which you will also obtain shortly).

*Create a Database userL* 
-   This is the same user you will use when you do python manage.py createsuperuser and therefore the same superuser that you use to login to your /admin/ endpoint, so make sure to write it down. 
-   ALso, for security purposes and since we now have a Database in the cloud -- it is good practice to make sure you use viable username & passwords >= 13 alphanumeric characters. 
-   You should also put a legitimate email address when you do "createsuperuser" incase you forget it :)
        
    *CMD:*
    `gcloud sql users create DATABASE_USERNAME \`
        `--instance INSTANCE_NAME \`
        `--password DATABASE_PASSWORD`
    Or, By way of Google cloud UI <link="">
        (a) Navigate to Cloud SQL "instance" page.
        (b) Go to the "Users" tab.
        (c) Click "Add User Account"
        (d) Enter a Username
        (e) Enter a Password (Write these down we're going to need them soon!)
        (f) Click "Add"
--END POSTGRES CREATE--
**Create Service Account with ADMIN level privelages for your Postgres DBMS.** (Note I just realized you could potentially select to use the same user account that is tied to your GCP account. However, Google Docs currently say to create a seperate service account so that is what I am suggesting you do as well.)
(a) Go to the Service accounts page of the Google Cloud Console.
(b) Go to the Service accounts page

(c) Select the project that contains your Cloud SQL instance.
(d) Click Create service account.
(e) In the Create service account dialog, enter a descriptive name for the service account.
(f) Change the Service account ID to a unique, recognizable value and then click Create.
(g) For Role, select one of the following roles, click Continue, and then click Done:
(h) Cloud SQL > Cloud SQL Client
(i) Cloud SQL > Cloud SQL Editor
(j) Cloud SQL > Cloud SQL Admin
Note: To create a service account with the required permissions, you must have resourcemanager.projects.setIamPolicy permission. This permission is included in the Project Owner, Project IAM Admin, and Organization Administrator roles.
You must also have enabled the Cloud SQL Admin API. If you are using the legacy project roles (Viewer, Editor, Owner), the service account must have at least the Editor role.
(k) Click the action menu for your new service account and then select Manage keys.
(l) Click the Add key drop-down menu and then click Create new key.
(m) Confirm that the key type is JSON and then click Create.
(n) The private key file is downloaded to your machine. You can move it to another location. Keep the key file secure.
--[End_Database_Admin_Creation]==

**Configure Database Settings!**
----------------------------------
let's now create & Set some environment variables in our local CMD lines for Local testing/Database access.
export DATABASE_NAME=DATABASE_NAME
export DATABASE_USER=DATABASE_USERNAME
export DATABASE_PASSWORD=DATABASE_PASSWORD
==[End_LOCAL_Database_CONFIG]==


# **Google Kubernetes Engine Configuration**
    In this tutorial, we represent our Kubernetes configuration in a SINGLE yaml file called polls.yaml. Note, this could be improved upon. Although it works and it will scale - it is good software engineering practice to use modular design principles and seperate your k8s configuration into "Service" and seperatly "Deployment". At the time that I am making this, there are not many examples out there that actually walk through the setup like I am doing for you but I have already started a second draft (revision) of my yaml configuration setup which will be on this git repo once I see that it works.

(a) Navigate to `polls.yaml` and find the key "image", underneath "containers". There is a comment there to replace <My_Project_ID> with your google cloud project ID. If you dont have this written down by now, you can get it again by doing `gcloud config list` and grabbing the value stored in project, or navigate back to your main GCP dashboard using the UI.

(b) Run the following command and *note* the value of `connectionName`:
`gcloud sql instances describe INSTANCE_NAME --format "value(connectionName)"`

(c) Since were here, let's go back to the `polls.yaml` file and replace <My-CloudSQL-connection-String> with the output from the previous command done in (b).

==[Congratulations!_the_CloudSQL_is_Now_CONFIGURRRRREEED!!():]==

# Run The App Locally!
We need two terminals open for this one. With our backend services now configured you can now run the app on your computer in development mode, create a superuser, and apply database migrations.
(a) In one of the 2 open terminals you have, we need to first start the Cloud SQL Auth Proxy:
`./cloud_sql_proxy -instances="PROJECT_ID:REGION:INSTANCE_NAME"=tcp:5432`
This step establishes a connection from your local computer to your Cloud SQL instance for local testing purposes. Keep the Cloud SQL Auth proxy running the entire time you test your app locally. Running this process in a separate terminal allows you to keep working while this process runs.

In a new terminal, set the Project ID locally:
`export GOOGLE_CLOUD_PROJECT=PROJECT_ID`
Run Makemigrations to and collectstatic to setup your models and static assets:
`python manage.py makemigrations`
`python manage.py makemigrations polls`
`python manage.py migrate`
`python manage.py collectstatic`
**Start your Server!, we're almost Finished!**

# -----
# To run locally, you need to open up 2-terminals:
# one to run our Cloud-Proxy, and another to run ./manage.py runserver:
#
# CMD1:
# --- 
# ./cloud_sql_proxy -instances="django-k8s-331621:us-west1:k8s-1"=tcp:5432
# CMD2:
# ---
# ./manage.py runserver


*Django Admin COnfiguration* 
-----------------------------
This is the part where we use those credentials we created earlier to setup our superuser with our local database. Note that unless you have Django environment variables installed, you won't have the dynamic user+password in your settings.py. Those can be hard-coded for the time being and are the same username, db-name, and db-pass from google cloudSQL.
<mysite>/settings.py:

Comment out the OLD SQLite3 database configuration and paste this code along with your details:
*DATABASES = {
    default': {
*# If you are using Cloud SQL for MySQL rather than PostgreSQL, set*
*# 'ENGINE': 'django.db.backends.mysql' instead of the following.*

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<MY_POSTGRES_DB_NAME>',
        'USER': '<MY_POSTGRES_USER_NAME>',
        'PASSWORD': '<MY_POSTGRES_DB_PA$$WORD>',
        'HOST': '127.0.0.1',
        'PORT': '5432',     # the port that postgres uses to recieve requests, leave this alone
    }
}*
(a) `python manage.py createsuperuser` (DONT FORGET TO give legitamete email address incase you forget it LOL, last warning..)
(b) After you've made sure settings.py is referencing postgres correctly with gcloudSQL username and passwords, run the developemnt server again.
`python manage.py runserver`
(c) Login to your Admin Dashboard and check to see if your user and models exist (They should if you migrated when everyone else did..)


*Deploy your Django Web app to Google Kubernetes Engine (GKE).
When the app is deployed to Google Cloud, it uses the Gunicorn Server that we specified in our DOckerFile to create our DOcker_Image. You may or may not know this, but Django kinda sucks at serving static content because the way it handles caching static files (CSS, JS, Media) is by way of aggresivly caching on its WSGI server that only comes with a single worker listening for requests. using Gunicorn, we can ask the server to have 9 workers listening for requests such that it would take quite a bit more usage to create bottleneck or crash our site. What we also can do is use another server utility to handle our static content completely seperatly to make it even more lightweight/faster. Popular way of doing this is through a service known as NginX, but because Google makes this settup really easy - we can use their service known as GSUTIL which uses Cloud Storage to serve static content. Now pretty much all of our resources will be hosting in K8s cluster in the cloud. To recape we now have our POstgres Database, Gunicorn Server and we're are now implementing our Cloud based storage through gsutil!

(1) Collect and upload your static files: 
    = this command will create a Cloud Storage bucket and make it publicaclly readable:
    `gsutil mb gs://PROJECT_ID_MEDIA_BUCKET`
    `gsutil defacl set public-read gs://PROJECT_ID_MEDIA_BUCKET`

Gather all the static content locally into one folder:
`python manage.py collectstatic`

Upload the static content to Cloud Storage:
`gsutil -m rsync -r ./static gs://PROJECT_ID_MEDIA_BUCKET/static`

In mysite/settings.py, set the value of STATIC_URL to the following URL, replacing [YOUR_GCS_BUCKET] with your bucket name:
`http://storage.googleapis.com/PROJECT_ID_MEDIA_BUCKET/static/`

==[Thats that, now your static content will be stored in the cloud!]==

# Set up GKE (ooohh ya)
(1) To initialize GKE, go to the Clusters page Under Google Kubernetes Engine (GKE):
<link="https://console.cloud.google.com/kubernetes/list?_ga=2.166569982.1148220492.1636612663-1560281031.1634941120&_gac=1.146556614.1634974855.CjwKCAjwwsmLBhACEiwANq-tXKEARSvBE_6hw5H61r35YO259FO4o025i6bwFpgddaj82kAzTqUNRxoCqRUQAvD_BwE">

*Note: If this is your first project using Google CLoud or GKE, it may take a few minutes for your project to be ready. You need to wait for your project on GKE to say "Kubernetes Engine is getting ready. This may take a minute or more" to disappear before moving forward to steps (2) (3) in this Section (set up GKE).

gcloud container clusters create polls \
  --scopes "https://www.googleapis.com/auth/userinfo.email","cloud-platform" \
  --num-nodes 4 --zone "[us-central1-a]"

  # Tip: When you setup Projectes anywhere on Google CLoud you should make sure the zone you choose is the same accross the various parts of your project. Ig you do not keep this uniform and you start obtaining traffic you may incurr more charges than you wanted. Change the [us-central1-a] to match your local region and the rest of your project to minimize cost of having your project hosted in the Cloud.
(2) 


(3) 

**DEPLOY Web app on GKE with HTTPS Redirect using Lets Encrypt: https://www.cloudskillsboost.google/focuses/2771?parent=catalog**