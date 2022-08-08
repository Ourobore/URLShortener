# URLShortener
A small URL shortener in Django.

With this app, you can easily shorten any URL: just enter the URL to short in the form, and submit. You will receive the shortened URL that will redirect to the desired URL.

This app is just a small project, and could be improved in many points. The goal was not to make a fully finished product, but more to understand how URL shorteners work in general, learn Django, do test driven development, and think about scalability while coding.

<br/>

**Disclaimer**: this app is not supposed to be used in production in this state. Especially because because it's using the [Django `runserver` command](https://docs.djangoproject.com/en/4.0/ref/django-admin/#runserver), that is not safe for a production environment.

<br/>

## How to run the app

### Docker Compose
First, create a `.env` file with the variables needed by the app (see `Environment variables` field below for more info). You must also have [Docker](https://docs.docker.com/engine/) and [Docker Compose](https://docs.docker.com/compose/) installed.

<br/>

Then run the following command to build and run the app
``` bash
$ docker compose up --build
```

Finally, you must setup the PostgreSQL by doing an initial migration:
```
$ docker exec -it webshortener-web-1 bash
```
Followed by:
```
$ python manage.py migrate
```
<br/>

While in the container, you can also setup the Django admin panel by creating a superuser. It will be needed to manage generated short URLs. You can do that with this command (and following the prompt):
```
$ python manage.py createsuperuser
```

<br/>

### Locally
You can also run the app locally with the following commands. Before you must ensure you have PostgreSQL installed, and setuped with a user and database.

When this is done, you can create a [Python virtual environment](https://docs.python.org/3/library/venv.html) and activate it:
``` bash
$ python3 -m venv .venv
$ source .env/bin/activate
```

Then, install the app requirements in the virtual environment with [`pip`](https://pypi.org/project/pip):
``` bash
$ pip3 install -r requirements.txt
```

Finally, create the `.env` and start the Django server in a virtual environment with the setup variables exported (see `Environment variables` field below for more info):

``` bash
$ env $(cat .env) python3 manage.py runserver
```

You may also need need to setup your database with an initial migration and superuser user creation (see above on how to do that)
<br/>

<br/>

## Environment variables
The following envrionment variables are needed in a `.env` file to setup the Django server and PostgreSQL database. Replace their values with yours.

```
DJANGO_SECRET_KEY=my_super_secret_and_long_secret_key
PSQL_NAME=my_database_name
PSQL_USER=my_psql_user
PSQL_PASSWORD=my_psql_password
PSQL_HOST=my_psql_host
PSQL_PORT=my_psql_port
```

`PSQL_HOST` must be set to either `localhost` if running the app locally, or to the `db` service if using Docjer Compose.