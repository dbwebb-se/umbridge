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


Database:
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

# Box view

[Boxes of architecture](https://lucid.app/lucidchart/invitations/accept/inv_dd2666ea-4863-460f-a482-79bedaa204d5?viewport_loc=-221%2C-767%2C3495%2C1687%2C0_0)
