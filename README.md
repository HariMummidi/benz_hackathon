# Python Microservice for Autonomus Driving Car to Estimate Travel Based on Current Charging and Distance

This project is for the Mercedes-Benz Research and Development Hackathon.
Hackathon Link: [https://www.techgig.com/hackathon/mercedes-benz-hiring-challenge](url) 

In this project I have,designed and implemented a microservice for an autonomous electric vehicle system with the following features:
    Check if the vehicle can reach the destination without charging.
    Find charging stations - If the destination can not be reached with current charging level. Appropriate handling to be done if the destination cannot be reached even with       charging

The features are described in detail below:

Check if vehicle can reach destination without charging

Created a microservice which exposes one REST endpoint(http://127.0.0.1:8080/merc/estimate_travel and can receive the request in the given request format.

`{ "vin": "vehicle identification number eg: W1K2062161F0014", "source": "source name", "destination": "destination name" }`

and the response format will be-

`{ "transactionId": "043020211 //A unique numerical value", "vin": "W1K2062161F0014 //vehicle identification number", "source": "source name", "destination": "destination name", "distance": "100 //distance between the source and destination in miles", "currentChargeLevel": "1 //current charge level in percentage , 0<=charge<=100", "isChargingRequired": "true/false //whether the vehicle has to stop for charging?.If true populate charging stations", "chargingStations": [ "s1", "s2" ], "errors": [ { "Id": 8888, "description": "Unable to reach the destination with the current charge level" }, { "id": 9999, "description": "Technical Exception" } ] }`

This will the give the result whether the vehical can reach the destination with the current charge level without charging at any charging stations in between the source and the destination.

## Installation and Setup
You can either build the docker image or pull the image from docker hub.
Below steps discuss on both the steps.

### Build the docker image from Dockerfile

Clone the repo to your local directory.

```
git clone https://github.com/HariMummidi/benz_hackathon.git/
```

```
[ravan@workstation ~]$ git clone https://github.com/HariMummidi/benz_hackathon.git/
Cloning into 'benz_hackathon'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (7/7), done.
remote: Total 12 (delta 2), reused 12 (delta 2), pack-reused 0
Unpacking objects: 100% (12/12), 2.58 KiB | 97.00 KiB/s, done.
```

```
cd benz_hackathon/
```

```
[ravan@workstation ~]$ cd benz_hackathon/
[ravan@workstation benz_hackathon]$ ls -lrth
total 20K
-rw-rw-r--. 1 ravan ravan  193 Oct  1 19:10 Dockerfile
-rw-rw-r--. 1 ravan ravan  391 Oct  1 19:10 README.md
-rw-rw-r--. 1 ravan ravan   31 Oct  1 19:10 requirements.txt
-rw-rw-r--. 1 ravan ravan 6.0K Oct  1 19:10 app.py
[ravan@workstation benz_hackathon]$
```

Once, repo is cloned to local directory run below commands to build the docker image

```
docker build . --tag benz_api
```

```
[ravan@workstation benz_hackathon]$ docker build . --tag benz_api
Sending build context to Docker daemon  82.94kB
Step 1/6 : FROM python:3.8-slim-buster
 ---> 319f36747aed
Step 2/6 : WORKDIR /app
 ---> Running in 2f5309e55cdb
Removing intermediate container 2f5309e55cdb
 ---> 212901a8bacc
Step 3/6 : COPY requirements.txt /app/requirements.txt
 ---> f12635b23d20
Step 4/6 : RUN pip3 install -r requirements.txt
 ---> Running in 42418b0dbe73
Collecting Flask==2.0.1
  Downloading Flask-2.0.1-py3-none-any.whl (94 kB)
Collecting requests==2.26.0
  Downloading requests-2.26.0-py2.py3-none-any.whl (62 kB)
Collecting Werkzeug>=2.0
  Downloading Werkzeug-2.0.1-py3-none-any.whl (288 kB)
Collecting click>=7.1.2
  Downloading click-8.0.1-py3-none-any.whl (97 kB)
Collecting itsdangerous>=2.0
  Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting Jinja2>=3.0
  Downloading Jinja2-3.0.1-py3-none-any.whl (133 kB)
Collecting urllib3<1.27,>=1.21.1
  Downloading urllib3-1.26.7-py2.py3-none-any.whl (138 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2021.5.30-py2.py3-none-any.whl (145 kB)
Collecting charset-normalizer~=2.0.0
  Downloading charset_normalizer-2.0.6-py3-none-any.whl (37 kB)
Collecting idna<4,>=2.5
  Downloading idna-3.2-py3-none-any.whl (59 kB)
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.0.1-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (30 kB)
Installing collected packages: MarkupSafe, Werkzeug, urllib3, Jinja2, itsdangerous, idna, click, charset-normalizer, certifi, requests, Flask
Successfully installed Flask-2.0.1 Jinja2-3.0.1 MarkupSafe-2.0.1 Werkzeug-2.0.1 certifi-2021.5.30 charset-normalizer-2.0.6 click-8.0.1 idna-3.2 itsdangerous-2.0.1 requests-2.26.0 urllib3-1.26.7
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container 42418b0dbe73
 ---> c41687b23b02
Step 5/6 : COPY . /app
 ---> b8cb85abe93e
Step 6/6 : CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
 ---> Running in c8923b185723
Removing intermediate container c8923b185723
 ---> d2ec53dc4e82
Successfully built d2ec53dc4e82
Successfully tagged benz_api:latest

```


### Pull repo from Docker hub

Pull the image from Docker Hub repo ravaan007/hackathons

```
docker pull ravaan007/hackathons:benz_microservice_api
```


```
[ravan@workstation benz_hackathon]$ docker pull ravaan007/hackathons:benz_microservice_api
benz_microservice_api: Pulling from ravaan007/hackathons
07aded7c29c6: Already exists 
1242903d2b23: Already exists 
6feb96d3e4f9: Already exists 
36bf03acdc50: Already exists 
366f5e2f7043: Already exists 
37b102b77035: Pull complete 
0ee4578496bb: Pull complete 
4cdcd8cc8f39: Pull complete 
e8188c4c1b0c: Pull complete 
Digest: sha256:15d9af3ca35e94ca4701461cacbd06bd756f92691d7795ff67c12f65ab0def7d
Status: Downloaded newer image for ravaan007/hackathons:benz_microservice_api
docker.io/ravaan007/hackathons:benz_microservice_api
[ravan@workstation benz_hackathon]$ 

```

## Running Docker Container

Once docker image is build from dockerfile or pull from repo
Run the docker container from the image, which will run the container in background.

**Steps for running from build image:**

```
docker container run -d -p 8080:5000 benz_api
```

```
[ravan@workstation benz_hackathon]$ docker container run -d -p 8080:5000 benz_api
e4d33f6501f8df924665c1e12830c7ec0dfcd2c6467899aa40b8b1e8c82a7ae6
[ravan@workstation benz_hackathon]$
```

**Steps to run from Pulled image:**

```
[ravan@workstation benz_hackathon]$ docker container run -d -p 8080:5000 ravaan007/hackathons:benz_microservice_api
339b150978fc72496f7460e3064dfb6a6847c373ef3308e9e6991309a183dde9
[ravan@workstation benz_hackathon]$
```

## Validation

Once docker container is up and running, ran below 5 Test cases to validate

**Test Case: 1**
Input : ```{ "vin": "W1K2062161F0033", "source": "Home", "destination": "Lake" }```


Output:

![image](https://user-images.githubusercontent.com/85939709/135659732-1af6798b-3429-4d52-af97-379024c49164.png)

**Test Case: 2**
Input : ```{ "vin": "W1K2062161F0080", "source": "Home", "destination": "Airport" }```


Output:

![image](https://user-images.githubusercontent.com/85939709/135660334-d0d36b7c-4d71-4742-9bd8-389f47e4a610.png)


**Test Case: 3**
Input: ```{ "vin": "W1K2062161F0080", "source": "@$%%%", "destination": "Airport" }```


Output:

![image](https://user-images.githubusercontent.com/85939709/135660573-44380e9e-f3d2-4666-a1bb-d7cf953bfd1c.png)

**Test Case: 4**

Input: ```{ "vin": "W1K2062161F0046", "source": "Home", "destination": "Movie Theatre" }```


Output:

![image](https://user-images.githubusercontent.com/85939709/135660863-cf651033-db36-4077-9d7a-56d35ad026c3.png)

**Test Case: 5**
Input: ```{  "vin": "W1K2062161F0014", "source": "Home", "destination": "Zoo"  }```


Output:

![image](https://user-images.githubusercontent.com/85939709/135661459-abd77bac-cf41-4d4c-9e2f-15efcbb9de4c.png)


