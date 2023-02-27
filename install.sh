python -m pip install -r requirements.txt
mkdir -p /etc/listflowbot
groupadd listflowbot
useradd -g listflowbot listflowbot
cp listflowbot /bin/
chmod a+x /bin/listflowbot
cp main.conf /etc/listflowbot/main.conf
cp main.py /etc/listflowbot
cp functions.py /etc/listflowbot
cp listflowbot.py /etc/listflowbot
chmod +x /etc/listflowbot/listflowbot.py
chmod a+x /etc/listflowbot
file=/etc/systemd/system/listflowbot.service
if test -f "$file"; then
    service listflowbot stop
    rm -f /etc/systemd/system/listflowbot.service
    systemctl daemon-reload
fi
cp listflowbot.service /etc/systemd/system/listflowbot.service
systemctl daemon-reload

systemctl enable listflowbot