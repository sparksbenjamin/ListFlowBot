service listflowbot stop
cp listflowbot /bin/
chmod a+x /bin/listflowbot
cp main.py /etc/listflowbot
cp functions.py /etc/listflowbot
cp listflowbot.py /etc/listflowbot
chmod +x /etc/listflowbot/listflowbot.py
chmod a+x /etc/listflowbot
rm -f /etc/systemd/system/listflowbot.service
systemctl daemon-reload
cp listflowbot.service /etc/systemd/system/listflowbot.service
systemctl daemon-reload

systemctl enable listflowbot
service listflowbot start