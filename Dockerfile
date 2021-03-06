FROM ubuntu

WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

# Update the sources list
RUN apt-get update \
 && apt-get update -y \
 && apt-get install -y python3-pip libpq-dev python3-dev \
 && cd /usr/local/bin \
 && ln -s /usr/bin/python3 python \
 && pip3 install --upgrade pip setuptools wheel \
 && apt-get install -y libmysqlclient-dev \
 && apt-get install -y cups

# Configure the python requirements
COPY . /srv/reagent_db/server/
WORKDIR /srv/reagent_db/server

COPY printers.conf /etc/cups/

RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade -r requirements.txt
EXPOSE 5000
# CMD ["python3", "main.py", "--dbhost", "10.0.2.2"]
CMD service cups start && python3 main.py --dbhost 10.0.2.2