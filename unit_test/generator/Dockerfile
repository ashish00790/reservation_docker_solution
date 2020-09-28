#Dockerfile
FROM python:3.6

WORKDIR /usr/app

ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./

ADD app.py /
ADD reservations.py /
ENTRYPOINT ["python", "/app.py"]