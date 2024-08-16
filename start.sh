# run migrations
python -m manage makemigrations
python -m manage migrate
python -m manage makemigrations user
python -m manage makemigrations search
python -m manage migrate user
python -m manage migrate search

# load user seed
python manage.py loaddata seed/users.json

# python -m manage graphql_schema --schema user.gq.schema.schema --out schema.graphql

# start app
python -m manage runserver 0.0.0.0:8000
