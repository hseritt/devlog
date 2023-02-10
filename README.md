# devlog

## Development

### How to Create an App

We keep apps inside of a toplevel folder called apps. You can then pull the apps modules in by:

```python
from apps.appname.models import MyModel
```

With that in mind, create them like so:

```bash
mkdir apps/appname
./manage.py startapp appname apps/appname
```

Add 'apps.appname' to INSTALLED_APPS in config/settings.py

Change app name in apps/appname/apps.py to use 'apps.appname' instead of just 'appname'.

### Scripts

- reset.sh - Resets data for project. It dumps current data to a fixture file. Recreates a postgres database, runs migrations and then imports the dumped data back into the database. This can be error-prone but by default it does backup your data set to fixtures/backups so that you can find your last good backup. You could then run:

```
python manage.py loaddata <last good backup file>
```

- runserver.sh - Runs the Django dev server.
