FROM ubuntu

RUN apt-get update

RUN apt-get install -y python3

RUN apt-get install -y python3-pip

COPY bot.py requirements.txt /opt/

RUN pip3 install -r /opt/requirements.txt

CMD ["python3", "/opt/bot.py"]
