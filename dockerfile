FROM python:latest
COPY install/requirements.txt   /root/requirements.txt
COPY listflow_docker.py /root/listflow_docker.py
COPY run.sh /root/run.sh


CMD ["bash", "/root/run.sh"]


