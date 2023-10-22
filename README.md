# 🚀 CERN Recruitment Challenge 🚀


Welcome to my submisson. I am thrilled to have you here. 😄


### Project Description

The follwoing repository contains Andrei Geadau's submission for CERN - SY-EPC-CCS - Full Stack Coding Challenge, where the aim is to add features to an existing simplified meal ordering platform. 😎

### Screenshots

![image](https://res.cloudinary.com/dbzyrdxlm/image/upload/v1697968713/bpkkkq4qflztoaf0prqu.png)
![image](https://res.cloudinary.com/dbzyrdxlm/image/upload/v1697968713/o6c9kiytakhlk1m32kps.png)
![image](https://res.cloudinary.com/dbzyrdxlm/image/upload/v1697968713/bvtqbi6tpdc0wplvjkey.png)


### Features

#### 1. **User Authentication:**
   - 🌈 Login, registration **and logout** functionality
   - 🎉 Form (email, password) validation
   - 🚀 Back-end and front-end tests


#### 2. **Dish Orders:**
   - 🎉 Shopping cart functionality (including adding and removing items)
   - 🔥 Back-end tests

#### 3. **Dish Reviews:**
   - 🌐 User reviewing ordered dishes functionality:
   - 🌟 Users view average rating 🌟
   - Constraint: One user only gives one review per dish, and only after having ordered that dish.
   - Reviews (rating and comments) are persisted in the database. 
   - 🔥 Back-end tests

#### 4. **User-Restaurant Chat:**
   - ✨ Interactive chat feature between user and restaurant employee.
   - 🌐 Allows users to:
      1. Initiate and end chat conversations.
      2. The chat automatically ends if the customer is inactive for 10 seconds

#### 5. **Order Page:**

   - 🌈 Users can only view their own order history.
   - 🔥 Order tracking feature that allows to view the status/progress of a user's orders.
   - 👍 The state machine can be seen below (also in `/img` folder):
     ![image](https://res.cloudinary.com/dbzyrdxlm/image/upload/v1697968691/vmyfqpygxcxuna1usl4r.jpg)
   - ✨ Design choises:
     1. an order can only be CANCELLED from SUBMITTED and ACCEPTED states
     2. a REJECTED / CANCELLED represent final states, aka cannot be changed anymore
   -  🌟 For simplicity, users can trigger all actions in the UI, but these actions adhere to the state transitions defined above.
   -   🎉 Back-end tests

### How to run the app
We assume you have docker desktop installed. Next, run the setup script which will create a docker volume and create SSL certificates for you to develop locally your app (follow the instructions given by the `setup.sh` script):

`./scripts/setup.sh`

After doing so, just run the following command to run the current application stack:

`docker compose --profile app up -d`

This command will launch 4 containers:
- Python server using FastAPI framework
- Vue client development server
- Postgres Database
- Traefik Proxy

You will be able to access:
- Client: `https://localhost:8443/client/`
- Server API: `https://localhost:8443/api`
- Server Docs: `https://localhost:8443/api/docs`


### How to run the tests

#### Back-end tests
`docker conainer ls`

`docker exec -it [SERVER_CONTAINER] /bin/bash`

`python3 -m pytest -rP`

#### Front-end tests
`npx cypress run`


### Rules
- Please implement your solution with the Vue.js (v3) and FastAPI frameworks.
- Please only use packages that are being shipped with this challenge. This concerns both, front-end and back-end. For example, the front-end includes the packages `primeflex`, `primeicons` and `primevue` which should be sufficient for completing this challenge.

### Submission
- Please submit your solution as a zip file. It should contain the entire repository, including your .git folder.
- Please name your zip file by the following format: firstname_lastname.zip, where firstname is your first name and lastname is your last name.
- Please make sure to submit your solution before the deadline. The deadline as well as the location for the submission are mentioned in the e-Mail which invited you to this challenge.
