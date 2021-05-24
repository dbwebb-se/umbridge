### Run application

Start byt setting the FLASK_APP and FLASK_ENV env vars:
```
export FLASK_APP=umbridge.py
export FLASK_ENV=development
```

Available environments:
```
development
production
test
```

Start the app with the following command and go to `localhost:5000` in your browser.
```
flask run
```

Available routes:

```
/wall-e
/eve
```


### Database:
Setup SQLite database if `migrations` folder already exist:
```
flask db upgrade
```

If you have upgraded the code for any SQLAlchemy models:
```
flask db migrate -m '<message>'
flask db upgrade
```

If you need to recreate app.db and migrations folder:
```
flask db init
flask db migrate -m '<message>'
flask db upgrade
```

If you have the wrong migrations version in the database when you want to upgrade it you can change it with:
```
flask db stamp head
flask db upgrade
```

### Test configuration:
As `dbwebb test` can vary, inside `app/eve/config/course_map.json` lies a configuration file.
You can override the `default` configurations for a course by adding a new object matching the course's name. Example:
```json
{
    "python": {
        "log_file": ".log/test/{kmom}.log",
    },
    "default": {
        "git_url": "https://github.com/dbwebb-se/{course}.git",
        "dbwebb_test_command": "dbwebb test --docker {kmom} {acr} --download",
        "log_file": ".log/test/docker/main.ansi"
    }
}
```

This will change the log file's location from the default value.  

Supported string substitutions are:
 * `{course}`  - will be replaced with the assignments course.
 * `{kmom}`    - will be replaced with the assignments kmom.
 * `{acr}`     - will be replaced with the students acronym.

# Box view

[Boxes of architecture](https://lucid.app/lucidchart/invitations/accept/inv_dd2666ea-4863-460f-a482-79bedaa204d5?viewport_loc=-221%2C-767%2C3495%2C1687%2C0_0)
