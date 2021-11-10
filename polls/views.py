# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse

# Note:
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

def index(request):
    return HttpResponse("<h1>Hello, Kubernetes!!</h1> <p>Let's Gooo!</p>.")
