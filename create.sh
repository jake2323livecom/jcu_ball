docker-compose up -d --build
sleep 2.0
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
