# ParcelLocker
![Python 3.12.4 Badge](https://img.shields.io/badge/python-3.12.4-blue?logo=python&logoColor=white&labelColor=black) 
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)](https://dzony97.github.io/ParcelLocker/htmlcov/index.html)
![Type Checking](https://img.shields.io/badge/type_check-mypy-blue) 
![MySQL](https://img.shields.io/badge/database-MySQL-blue?logo=mysql&logoColor=white&labelColor=black)
![Docker Compose](https://img.shields.io/badge/docker--compose-2496ED?logo=docker&logoColor=white&labelColor=black)


## Description
ParcelLocker is a Python-based application that leverages MySQL for database management to streamline package delivery and pickup. This application enables users to send and receive packages conveniently, as well as locate the nearest available parcel lockers, making logistics simpler and more accessible

### Requirements

- Python 3.12.4
- Docker (for Docker Compose)
- Pipenv (for dependency management)

### Steps to Set Up

1. **Clone the Repository**

Clone the repository to your local machine:
```bash
git clone https://github.com/Dzony97/ParcelLocker.git
```

2. **Set Up a Virtual Environment**

Open Command Prompt or PowerShell.
Navigate to your project directory.
Run the following commands:
```bash
pip install pipenv
pipenv shell
pipenv install
```

3. **Build and Run with Docker Compose**
   
Use Docker Compose to build and run the project:
```bash
docker-compose up --build
```

4. **Run the Application**

If the project requires running a main function, execute it:
```bash
pipenv run python main.py
```
