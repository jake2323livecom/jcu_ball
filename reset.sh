docker-compose down -v
docker rmi jcu_ball_web
docker rmi jcu_ball_nginx
docker-compose up -d --build
sleep 1
