# ParcelLocker
![Python 3.13](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white&labelColor=black) 
![Flask](https://img.shields.io/badge/framework-Flask-blue?logo=flask&logoColor=white&labelColor=black) 
![Pydantic](https://img.shields.io/badge/validation-Pydantic-blue?logo=pydantic&logoColor=white&labelColor=black) 
![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen) 
![Type Checking](https://img.shields.io/badge/type_check-mypy-blue) 
![MySQL](https://img.shields.io/badge/database-MySQL-blue?logo=mysql&logoColor=white&labelColor=black) 
![Docker Compose](https://img.shields.io/badge/docker--compose-2496ED?logo=docker&logoColor=white&labelColor=black)




## Description
ParcelLocker is a Python-based web application built with Flask that leverages MySQL for database management to streamline package delivery and pickup. The application enables users to send and receive packages, as well as locate the nearest available parcel lockers, making logistics simpler and more accessible.

### Requirements

- Python 3.13
- Docker (for Docker Compose)
- Pipenv (for dependency management)
- Flask (as web framework)
- MySQL (for database management)
- Pydantic (for data validation)

### Steps to Set Up

1. **Clone the Repository**

Clone the repository to your local machine:
```bash
git clone https://github.com/Dzony97/ParcelLocker.git
```


2. **Set Up a Virtual Environment**

This project consists of three separate microservices, each with its own dependencies managed through Pipenv. To set up the virtual environments for each microservice, follow these steps:

#### a. **For users:**

1. Open Command Prompt or PowerShell.
2. Navigate to the `users` directory:
```bash
cd users
```
3. Install Pipenv and the necessary dependencies:
```bash
pip install pipenv
pipenv shell
pipenv install
```

#### a. **For parcel_lockers:**

1. Open Command Prompt or PowerShell.
2. Navigate to the `parcel_lockers` directory:
```bash
cd parcel_lockers
```
3. Install Pipenv and the necessary dependencies:
```bash
pip install pipenv
pipenv shell
pipenv install
```

#### a. **For api_gateway:**

1. Open Command Prompt or PowerShell.
2. Navigate to the `api_gateway` directory:
```bash
cd api_gateway
```
3. Install Pipenv and the necessary dependencies:
```bash
pip install pipenv
pipenv shell
pipenv install
```


3. **Build and Run with Docker Compose**
   
To run the application, use **Docker Compose** to start the microservices in separate containers. Follow these steps:

1. Make sure you have **Docker** and **Docker Compose** installed on your machine.
2. Navigate to the project root directory.
3. Start all microservices by running:
```bash
docker-compose up --build
```

4. **Run the Application**

Once the microservices are up and running, you can use Postman (or any other API client) to interact with the application by sending requests to the appropriate endpoints.

Open Postman.

Set the request type (GET, POST, PUT, DELETE, etc.) and enter the URL of the running microservice. For example, if you're running the application locally, the URL might look like:

```bash
http://localhost/clients/
```

### 5. **Blueprints**

The project is organized using **Flask Blueprints** to modularize different functionalities of the application. Below is a list of the available blueprints in the project:

- **Get Client Location**  
  Endpoint to retrieve the location of a client.
  - **URL**: `http://localhost/clients/<client_id>`
  - **Method**: `GET`

- **Get Packages**  
  Endpoint to retrieve details of a specific package.
  - **URL**: `http://localhost/packages/<package_id>`
  - **Method**: `GET`

- **Send Packages**  
  Endpoint to send a package.
  - **URL**: `http://localhost/packages`
  - **Method**: `POST`

- **Register User**  
  Endpoint to register a new user.
  - **URL**: `http://localhost/users/register`
  - **Method**: `POST`

- **Login User**  
  Endpoint to log in a user and retrieve a token.
  - **URL**: `http://localhost/users/login`
  - **Method**: `POST`

- **Refresh Token**  
  Endpoint to refresh an authentication token.
  - **URL**: `http://localhost/users/refresh`
  - **Method**: `POST`

- **Activate Token**  
  Endpoint to activate a user's token.
  - **URL**: `http://localhost/users/activate`
  - **Method**: `POST`

- **Add Parcel Locker**  
  Endpoint to add a new parcel locker.
  - **URL**: `http://localhost/parcel_lockers/parcel_locker`
  - **Method**: `POST`

- **Add Locker**  
  Endpoint to add a specific locker to the system.
  - **URL**: `http://localhost/parcel_lockers/locker`
  - **Method**: `POST`
