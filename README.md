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
/eve
  /reset - Resets the database and adds "Wall-E Kursen" to the course table
  /grade - Tests all "submitted" assignments
/wall-e
  /fetch-submissions - Fetches all submissions that are not graded
  /grade             - Grades the students 
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

#### Models
There are two database tables, `course` and `submission`. A `course` is required before adding `submissions`.

The `course` table contains:
  * `id` - The `course_id` from Canvas
  * `name` - The courses dbwebb name eg. "python" or "htmlphp".
  * `active` - If the course is active, wall-e will fetch submissions from it
    - 0, Not active
    - 1, Active

The `submission` table contains:
  * `id` - Auto generated primary key.
  * `user_id` - A students canvas id
  * `user_acronym` - The students acronym
  * `assignment_id` - The assignments canvas id
  * `kmom` - The assignments name
  * `course_id` - The course id (FK) to `course.id`
  * `course` - Pointer to the `course` based on `course_id`
  * `feedback` - Dbwebb test logfile content
  * `grade` - The grade of the assignment
     - `NULL`, not yet graded
     - `"Ux"`, one or more tests has failed
     - `"PG"`, all tests passed
  * `workflow_state` - Follows the CanvasAPI standards and represents the current status of an assignment
     - `"submitted"`, recently fetched by wall-e
     - `"pending_review"` has been tested by eve
     - `"graded"`, grade has been reported to canvas


### Test configuration:
There is a configuration file inside `app/settings/course_map.json`. This is used to configure the default behavior depending on the course. If a course is missing a key or does not exist it will fallback to the default values.

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

This will change the log file's location for the python course.

Supported keys are:
 * `git_url` - The link to the course repo.
 * `dbwebb_test_command` - The command used to test the assignment.
 * `log_file` - The file that will be sent to the students upon grading.

Supported string substitutions are:
 * `{course}`  - will be replaced with the assignments course.
 * `{kmom}`    - will be replaced with the assignments kmom.
 * `{acr}`     - will be replaced with the students acronym.

# Box view

[Boxes of architecture](https://lucid.app/lucidchart/invitations/accept/inv_dd2666ea-4863-460f-a482-79bedaa204d5?viewport_loc=-221%2C-767%2C3495%2C1687%2C0_0)
