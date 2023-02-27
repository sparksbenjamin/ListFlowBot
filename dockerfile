FROM python:3
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY install/requirements.txt   ./

RUN pip install --no-cache-dir -r requirements.txt
COPY listflow_docker.py ./
CMD [ "python", "listflow_docker.py" ]
