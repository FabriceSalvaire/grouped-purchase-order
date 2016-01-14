rm db.sqlite3
rm GroupedPurchaseOrder/migrations/*.py

manage.py makemigrations
manage.py migrate
manage.py makemigrations GroupedPurchaseOrder
manage.py makemigrations django_messages # ?
manage.py migrate
manage.py loaddata GroupedPurchaseOrder/fixtures/demo.json
sqlite3 db.sqlite3 < tools/set-superuser.sql

# manage.py createsuperuser
# manage.py runserver
