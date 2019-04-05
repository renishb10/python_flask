FROM ubuntu:latest

LABEL company=GlobalEnglish \
    developers=Renish

RUN apt-get update -y && \
    apt-get install -y python3.7 python3-pip python-dev

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN python3.7 -m pip install -r requirements.txt

RUN python3.7 -V
RUN pip3 freeze

COPY . /app

# expose the port to outside world
EXPOSE  5000

CMD [ "python3.7", "./run.py" ]