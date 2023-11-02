# 2fa-microservice
A microservice providing 2FA


## Installation

### Local
The project requires python version 3.11 to be avilable.
To install the app, you will need install [poetry](https://python-poetry.org/docs/#installation). The lock file was generated in version 1.1.14, so same version must be used.
```bash
curl -sSL https://install.python-poetry.org | python3 - --version 1.1.14
```
Having poetry running, you can install the dependencies and the app:
```bash
poetry install
```
You're done! Now you can run the application and test it.

### Docker
The setup can be done without installing anything, using docker-compose.


## Running application
In order to make everything work, setup all the required secrets in `envs/.local` dotenv file (for local development) ot in `envs/.docker` if you're planning to run the application with docker.
### Local
No matter you use docker-compose or you run server locally, you have to make redis container running. To do so, run:
```bash
docker-compose up -d redis
```
Then, just exec the command (from the root of the repository)
```bash
poetry run app/main.py
```
The application will be avilable on `localhost:8000`.

### Docker
To run application in docker, just exec:
```bash
docker-compose up -d
```
The application should be avilable on the port 8000.

## Testing
To run tests, you have to have local setup done. Then, you can exec:
```bash
poetry run pytest tests
```
Disclaimer: running integration tests require redis container to be running.

## What else could be done
* Authentication
It wasn't listed as a part of requirements, but might be needed. There are various methods, including defining access rules inside of the k8s cluster (with ingress), so the implementation strongly depends on the business requirements.

* Authentication to Vonage
In real life scenario, I would prefer to generate token (possible with vonage api).

* Deployment workflow
Depending on the container repository and business requirements, there should be a workflow that builds and pushes image to repository.
* Improved phone validation
Depending on the business requirements, I would add a better validation.


# tencacity retry?
