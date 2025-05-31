set -o errexit

pip install -r requirements.txt

python backend/myauth/manage.py migrate
python backend/myauth/manage.py collectstatic --no-input