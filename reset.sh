docker-compose down -v
docker rmi $(pwd)_web
docker rmi $(pwd)_nginx
docker-compose up -d --build
sleep 1
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
