# Locust demo

[Locust](http://www.locust.io/) is an open source load-testing tool in which the user behaviour is defined in Python. Tests can be run and monitored via the CLI or the dedicated UI.

## Prerequisites

- Python 3.11
- Poetry

## Local set-up

- From both `/api` and `/locust-testing` folders run:

```bash
poetry config virtualenvs.in-project true
poetry install
```

- From the `/api` folder run:

```bash
poetry run uvicorn main:app --reload
````

- From `/locust` folder run:

```bash
poetry run locust --host="http://localhost:8000 --class-picker"
```

- Navigate to [http://localhost:8089](http://localhost:8089), enter the number of users and spawn rate and hit "start swarming" !

- To launch the tests _via_ the CLI only run:

```bash
poetry run locust --headless --users [number-of-users] --spawn-rate [number] -H http://localhost:8000/
```

## Production set-up and Identity Aware Proxy

Locust can be deployed in the cloud and run as a separate service. A Dockerfile is available for that purpose (running Locust UI version).

If the service to be tested runs behind IAP you will need to authorize the Locust service's service account as IAP web-app user, and fill in the service to be tested OAuth 2.0 client ID in the corresponding field of Locust UI.