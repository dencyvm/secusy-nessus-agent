# syntax=docker/dockerfile:1
FROM python:3.10
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install libpcap-dev -y


WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
COPY . .

# Copy the current directory contents into the container at /
# COPY engine-nessus.py .
# COPY parser.py .
# COPY nessus.json .
# COPY requirements.txt .


# COPY . /etc/ /etc/
# COPY . nessus/etc/

# RUN pip install -r requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# WORKDIR /code/nessus/ext-libraries/
# RUN git clone https://github.com/tenable/nessrest
# RUN cd nessrest && git reset --hard af28834d6253db0d00e3ab46ab259dd5bc903063
WORKDIR /code/nessus/ext_libraries/nessrest/
RUN pip install -r requirements.txt
# RUN git apply /code/nessus/etc/ness6rest.patch  --reject --ignore-space-change --ignore-whitespace
# git apply --ignore-space-change --ignore-whitespace
# RUN pip3 install --trusted-host pypi.python.org -e /code/nessus/ext-libraries/nessrest/
WORKDIR /code