# Migrations with Django
- [Django's migration documentation](https://docs.djangoproject.com/en/3.1/topics/migrations/)
- Before applying migrations in Django, we need to instruct Django to auto-generate the file detailing the migration.

## Using Docker
1. Open a terminal inside the ```backend``` container.
```bash
docker container exec -it <container name> bash
```
2. Activate the python virtual environment from inside the container.
```bash
source src/venv/bin/activate
```
3. Navigate to the ```/app``` folder in the source code
```bash
cd src/app
```
4. Run the ```makemigrations``` command
```bash
python manage.py makemigrations
```