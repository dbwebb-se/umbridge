Umbridge
================================

Automatic grading system that utilizes the [canvas api](https://canvas.instructure.com/doc/api/). It is primarily built for the [dbwebb-cli](https://github.com/dbwebb-se/dbwebb-cli) and its courses.



#### Installation

```bash
# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install pip requeirements
make install
```



### Run application

Start by setting the env vars. Create `.env` in project root folder and add all except `FLASK_APP`, it need to be added globally:
```bash
export FLASK_APP=umbridge.py
export FLASK_ENV=development
export TOKEN_CANVAS_API={Your Canvas token}
export URL_CANVAS_API={The Base URL to the canvas api} # defults to `'https://bth.instructure.com'`.
export HOST={The server base_url} # defults to `'http://localhost:5000'`.
export SECRET_KEY="<a secret flask string>"
export CREDENTIALS="<base64 of username:password>"
export UMBRIDGE_ENV=true/false
```

If using special umbridge user for dbwebb, export `UMBRIDGE_ENV=true`.

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
  /fetch-submissions - Fetches all submissions that are not graded from canvas and adds them to the database as 'submitted'. Returns a redirect to `eve/test/`
  /grade             - Grades the students


/eve
  /reset - Resets the database and adds "Wall-E Kursen" to the course table
  /test - Tests all "submitted" assignments as well as updates them with the test results, their grade and the workflow_state to "pending review". Returns a redirect to `/wall-e/grade`


/courses 
  ['GET'] - Gets courses
  ['POST'] - Adds a new course
  ['POST'] - Updates a course
  ['DELETE'] - Removes a course


/results
  /feedback/<log_id: string> - Displays the feedback log, `log_id` is the submissions' `uuid` with its `id` concatenated ("{uuid}{id}") at the end on the small off chance the uuid is a duplicate.
  /browse/<?req_path: string> - Displays a filetree where the user can navigare around files, it utilizes highlight.js to display the code in colorcoding for almost any file-extention.
```

**Some** routes requires an `Authorization` header:
```
{ 'Authorization': 'Basic {credentials}' }
```

**More information** can be found in the api documentation:
1. [wall-e](/docs/api/wall-e.md)
2. [eve](/docs/api/eve.md)
3. [courses](/docs/api/courses.md)



### Execute the grading process:

Start the server and use `flask grade {credentials}` to fetch, test and report the grades to canvas.  
**Note**: `credentials` has a default value of the test user and will be removed on production.

Example of a cron job to correct the students every 5 minuts and clear folders that are older than 30 min in temp folder:
```bash
UMBRIDGE_CREDENTIAL=="<credentials>"
*/30 * * * * find /home/azureuser/git/umbridge/app/wall_e/temp/* -maxdepth 0 -type d -mmin +30  | xargs rm -rf >/dev/null 2>&1
*/5 * * * * cd /path/to/repo && venv/bin/flask grade $UMBRIDGE_CREDENTIAL
0 */1 * * * sh /path/to/repo/backup_db.sh
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
flask db migrate
flask db upgrade
```

If you have the wrong migrations version in the database when you want to upgrade it you can change it with:
```
flask db stamp head
flask db upgrade
```



#### Models

There are three database tables, `course`, `submission` and `user`. A `course` is required before adding `submissions`. `user` keeps information about authenticated users to access routes.

The `course` table contains:
  * `id` - The `course_id` from Canvas
  * `name` - The courses dbwebb name eg. "python" or "htmlphp".
  * `active` - If the course is active, wall-e will fetch submissions from it
    - `0`, Not active
    - `1`, Active

The `submission` table contains:
  * `id` - Auto generated primary key.
  * `uuid` - Auto generated uuid4 that are used to view feedback logs.
  * `user_id` - A students canvas id
  * `user_acronym` - The students acronym
  * `assignment_id` - The assignments canvas id
  * `assignment_name` - The assignments name (kmom)
  * `course_id` - The course id (FK) to `course.id`
  * `course` - Pointer to the `course` based on `course_id`
  * `feedback` - Dbwebb test logfile content
  * `grade` - The grade of the assignment
     - `NULL`, not yet graded
     - `"Ux"`, one or more tests has failed
     - `"PG"`, all tests passed
  * `workflow_state` - Keeps track of the state, eg. if the submission needs to be tested or sent to canvas.
     - `"new"`, recently fetched by wall-e
     - `"tested"` has been tested by eve
     - `"graded"`, grade has been reported to canvas

The `user` table contains:
 * `id` - Auto generated primary key.
 * `username` - The username
 * `password_hash` - A hashed password, set this by calling `user.password = password`.



### App configuration for grading courses:

There is a configuration file inside `app/settings/course_map.json`. This is used to configure the default behavior depending on the course. If a course is missing a key or does not exist it will fallback to the default values. Commands need to be written in list with each argument as own element.

You can override the `default` configurations for a course by adding a new object matching the course's name. Example:
```json
{
    "python": {
        "ignore_assignments": [ "kmom02" ],
        "assignment_folders": {
            "kmom01": ["me/kmom01", "me/redovisa"],
            "kmom02": ["me/kmom02"],
            "kmom03": ["me/kmom03"],
            "kmom04": ["me/kmom04"],
            "kmom05": ["me/kmom05"],
            "kmom06": ["me/kmom06"],
            "kmom10": ["me/kmom10", "me/redovisa"],
            "exclude": ["__pycache__"]
      }
    },
    "default": {
      "git_url": "https://github.com/dbwebb-se/{course}.git",
      "installation_commands": [
          ["make", "docker-install"],
          ["dbwebb", "init-me"]
      ],
      "test_command": ["dbwebb", "test", "--docker", "{kmom}", "{acr}", "--download"],
      "update_command": ["dbwebb", "update"],
      "log_file": ".log/test/docker/test-results.ansi",
      "ignore_assignments": [],
      "assignment_folders": {
          "kmom01": ["me/kmom01"],
          "kmom02": ["me/kmom02"],
          "kmom03": ["me/kmom03"],
          "kmom04": ["me/kmom04"],
          "kmom05": ["me/kmom05"],
          "kmom06": ["me/kmom06"],
          "kmom10": ["me/kmom10"],
          "exclude": [""]
      }
    }
```

This will change so that courses with the name `"python"` will ignore correcting the canvas assignment `"kmom02"`.

Supported keys are:
 * `git_url` - The link to the course repo.
 * `test_command` - The command used to test the assignment.
 * `update_command` - The command used update the git repo before executing tests.
 * `log_file` - The file that will be sent to the students upon grading.
 * `installation_commands` - The steps taken when installing required dependencies.
 * `ignore_assignments` - A list of assignments to ignore.
 * `assignment_folders` - A dict with which directories are connected to what assignments. This is used to copy directories when zipping students code. Key is assignments name and value is a list with paths to directories which have code for the assignment. Also has key `exclude`, its value is a list with directory names to exclude when copying, e.g. cache dirs as `__pycache__`. Values in course specific dict can't be replace with values from default dict, all or nothing.

Supported string substitutions are:
 * `{course}` - will be replaced with the assignments course.
 * `{kmom}` - will be replaced with the canvas assignment name.
 * `{acr}` - will be replaced with the students acronym.



### Production

Run using the following Supervisorctl config for Gunicorn:

```
[program:umbridge]
environment=
    HOME="/home/<user>"
    FLASK_APP="umbridge.py"
command=<path-to-project>/umbridge/.venv/bin/gunicorn -b localhost:8000 -w 2 --access-logfile /var/log/umbridge/gunicorn-access.log --error-logfile /var/log/umbridge/gunicorn-error.log umbridge:app --timeout 1800 --worker-class sync
directory=<path-to-project>/umbridge
user=<user> # setting user doesnt include env vars, like setting correct HOME.
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

We need `--timeout 1800 --worker-class sync` to not timeout between correcting students. Set high timeout (30 min) so it shouldn't kill process when correcting many students but we still need it to kill the process if somethings hangs.


Gunicorn och Supervisorctl has problem with home dir. dbwebb reads config from root (`/`) instead of user home (`~/`). This is why we add HOME in config.



### Run application tests

There are several make commands for testing the application. Use make help to see which. To run all tests and validation use:

```
make test
```

# Box view

[Boxes of architecture](https://lucid.app/lucidchart/invitations/accept/inv_dd2666ea-4863-460f-a482-79bedaa204d5?viewport_loc=-221%2C-767%2C3495%2C1687%2C0_0)
