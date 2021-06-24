# Features
1. Update `dbwebb test` script for python to "auto potatoe" or update it for the new studserver user.
1. Create an endpoint that returns all assignments that has been corrected by both Umbridge and a teacher - *For an external php script that shows code*.
1. Show result log in php code view so students can see color codings?
1. Multiprocessing so can run multiple students at the same time?

# On prod
1. Remove the default token from `app/config.py`
1. Remove the default credentials from `app/__init__.py`
1. Remove the the route `eve/reset`


# other
1. user on canvas for credentials to connect to api. Needs to be added to all courses that use umbridge. If they don'nt want to create a new user, rewrite course model so every course has its own canvas API.


# Before students arrive

1. Change default user. 
1. Remove the default token from `app/config.py`
1. Remove the default credentials from `app/__init__.py`. Set password as env that crontab can use when calling grade.
1. Remove the the route `eve/reset`. Comment out
1. Ask for new user on canvas, otherwise do as above.
1. Create new python course.
1. Test IT's API. Use api to download students code so don't get problems with potatoe?
1. Build route for showing students code
1. Tell emil to reset his canvas token
