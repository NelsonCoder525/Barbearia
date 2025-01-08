set -o errexit

pip install -r requirements/prod.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [[$CREATE_SUPERUSER]];
then
    python manage.py createsuperuser --no-input
fi