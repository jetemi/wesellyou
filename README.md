# We Sell You (A sample project)
We sell you is a sample project.

## Usage
Have docker installed or download from [docker](https://docs.docker.com/engine/install/). Build the docker image for the first time using...

```bash
docker-compose build
```
then run the app
```bash
docker-compose up -d
```

## For the first run
1. You need to ensure that the database creates all the expected tables, so run
```bash
docker-compose exec web python manage.py migrate
```
2.  Then you can restart your app
```bash
docker-compose up -d
```