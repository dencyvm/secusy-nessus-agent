# syntax=docker/dockerfile:1
FROM python:3.10
# ENV PYTHONUNBUFFERED=1
# RUN apt-get update
# RUN apt-get install libpcap-dev -y
# RUN apt-get install masscan -y
# WORKDIR /code
# COPY requirements.txt /code/
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/


ENV MICRO_SERVICE=/home/app/code
# RUN addgroup -S $APP_USER && adduser -S $APP_USER -G $APP_USER
# set work directory


RUN mkdir -p $MICRO_SERVICE
RUN mkdir -p $MICRO_SERVICE/static

# where the code lives
WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update
RUN apt-get install libpcap-dev -y
#RUN apt-get install masscan -y
#RUN wget http://ftp.br.debian.org/debian/pool/main/m/masscan/masscan_1.3.2+ds1-1_amd64.deb
#RUN dpkg -i masscan_1.3.2+ds1-1_amd64.deb
# install dependencies
#RUN pip install --upgrade pip
# copy project
COPY . $MICRO_SERVICE
#RUN pip install -r requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
#WORKDIR $MICRO_SERVICE/nessus/ext_libraries/nessrest/
#RUN pip install -r requirements.txt

RUN apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]

WORKDIR $MICRO_SERVICE
COPY ./entry_point.sh entry_point.sh
RUN chmod +x entry_point.sh