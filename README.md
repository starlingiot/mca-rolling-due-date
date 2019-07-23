# Rolling Due Date
###### Medicine Creek Analytics

This is a prototype project that ingests Excel LIMS reports to create a dashboard for rolling due dates on sample tests.

It's built with Django, and uses local SQLite storage as a database. It uses Docker for convenience.

### Install

Just clone the repository, then run:

```
docker-compose up
```

The app is available on `http://localhost`!

If you don't have Docker, you can also use:

```
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py runserver
```

The app is now available on `http://localhost:8000`.


### Use

TODO

### Test

TODO

### Contribute

TODO

### License

TODO