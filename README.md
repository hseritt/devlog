# devlog

## Scripts

* reset.sh - Resets data for project. It dumps current data to a fixture file. Recreates a postgres database, runs migrations and then imports the dumped data back into the database. This can be error-prone but by default it does backup your data set to fixtures/backups so that you can find your last good backup. You could then run:

```
python manage.py loaddata <last good backup file>
```

* runserver.sh - Runs the Django dev server.
