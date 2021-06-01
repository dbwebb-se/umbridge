# Features
1. Write tests
    1. Unit
    2. Integration
3. Update `dbwebb test` script for python to "auto potatoe" and store output from other errors such as docker.

# On prod
1. Remove the default token from `app/config.py`
2. Remove the default credentials from `app/__init__.py`
3. Remove the the route `eve/reset`