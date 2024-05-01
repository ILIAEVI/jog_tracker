# Jogging Tracker API

This is a REST API built with Django REST Framework for tracking jogging times of users. 
The API allows users to create an account, log in, and manage their jogging records. 
It also supports different permission levels for users, user managers, and admins, ensuring appropriate access control.

## Features

- User authentication for all API calls
- Role-based access control with three roles: regular user, user manager, and admin
- CRUD operations for jogging records
- Integration with a weather API to fetch and store weather conditions for each run
- Weekly report generation for average speed and distance
- JSON format for data exchange
- Filtering and pagination capabilities for list endpoints
- Advanced filtering with support for operations precedence and combination of fields

## Technologies Used

- Django REST Framework
- Python
- Weather API
- PostgreSQL

## Getting Started

### Prerequisites

- Python
- Django
- Django REST Framework
- Weather API key


## Instructions:

#### Environment Configuration:
Ensure that you have an .env file in the project root directory with necessary environment variables. 
You can use the provided .env.example file as a template.


pip install -r requirements.txt

### Start Docker Desktop:
   #### Before proceeding with Django migrations, ensure that Docker Desktop is running on your system.
  #### Run the following command to build Docker containers defined in docker-compose.yml:

docker-compose build

docker-compose up -d

python manage.py migrate

python manage.py runserver