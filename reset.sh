docker-compose down -v
docker rmi jcu_ball_web
docker rmi jcu_ball_nginx
docker-compose up -d --build
sleep 1
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
