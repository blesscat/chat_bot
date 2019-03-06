docker run --rm -d -p 3000: -p 8000:80 -v "$PWD/nginx":/etc/nginx --name mynginx nginx
docker run --rm -d -p 5000:5000 -d --name telgram-bot blesscat/telegram-bot
