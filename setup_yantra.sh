sudo apt update -y
sudo apt upgrade -y

sudo apt install build-essential python3-dev git python3.12-venv nginx supervisor -y

# setup the firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx HTTP'
sudo ufw --force enable

APP_DIR=/home/book_user

# create a user to run the service
sudo adduser --comment --disabled-login --disabled-password book_user || true
cd $APP_DIR

# App install
sudo su book_user -c "git clone --depth 1  https://github.com/monera023/book-highlights-explorer.git"
touch book-highlights-explorer/debug.log
cd book-highlights-explorer/server
mkdir uploadFiles
sudo su book_user -c "python3 -m venv myenv; source myenv/bin/activate"
sudo su book_user -c "myenv/bin/pip3 install -r ../requirements.txt"

sudo tee -a /home/book_user/book-highlights-explorer/server/start_app.sh > /dev/null <<EOF
#!/bin/bash

export PYTHONPATH=/home/book_user/book-highlights-explorer:$PYTHONPATH
exec myenv/bin/python3 api_server.py
EOF

# Setup supervisor
sudo systemctl enable supervisor
sudo systemctl start supervisor
chmod +x start_app.sh
touch /etc/supervisor/conf.d/books-app.conf

sudo tee -a /etc/supervisor/conf.d/books-app.conf > /dev/null <<EOF
[program:book-highlight-app]
command=/home/book_user/book-highlights-explorer/server/start_app.sh
directory=/home/book_user/book-highlights-explorer/server
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/book_user/book-highlights-explorer/debug.log
EOF

# Start app using supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart book-highlight-app

# Setup nginx
touch /etc/nginx/sites-available/books-app

sudo tee -a /etc/nginx/sites-available/books-app > /dev/null <<EOF
server{
       listen 80;
       server_name <ip>;
       location / {
           include proxy_params;
           proxy_pass http://127.0.0.1:8000;
       }
}
EOF

sudo ln -s /etc/nginx/sites-available/books-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx