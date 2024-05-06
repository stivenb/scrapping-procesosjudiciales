# Web scrapping procesos judiciales Challenge

## Installation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt`
```


# INIT alembic
alembic init alembic
alembic revision --autogenerate -m "init models"
alembic upgrade heads


## Scaffolding and Architecture

The project follows a well-organized directory structure:

**api**: This directory contains the main API-related code.

**adapter**: Contains files that connect the service with external services from infrastructure.

**database**: Directory that potentially holds code related to database configuration, connections and models.

**domain**: Contains files representing the project's domain logic.

**infrastructure**: Contains files managing the technical infrastructure of the application.

**main.py**: The main API file where the FastAPI application is defined and configured.

**schemas**: Contains data schemas used for API incoming requests and outgoing responses.

**service**: Contains files connect the domain with particular uses cases for the API.

**settings.py**: File to store API configuration, such as environment variables, etc.

**tests**: Directory for automated API tests.

**utils**: Contains utility functions or common tools used in the application.

**scripts**: Contains scripts to help with the development process.

**Note**: This article is based on the following [article](https://douwevandermeij.medium.com/hexagonal-architecture-in-python-7468c2606b63).

**References**: Inspired by [refactoring](https://refactoring.guru/es/design-patterns/), [12factor](https://12factor.net/es/)