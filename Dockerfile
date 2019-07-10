##################################################################################
## Dockerfile to build the RK_LIMS server running the LIMS Reagents DB Web App
##################################################################################
FROM ubuntu

# Originally created by Bohdan Stebliy GitHub @BohSteb
MAINTAINER Bohdan Stebliy <Bohdan.Stebliy@uhnresearch.ca>

# Update the sources list
RUN apt-get update \
  && apt-get update -y \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && apt-get install -y libmysqlclient-dev \
  && apt-get install -y cups

# Configure the python requirements
COPY . /srv/RK_LIMS/server/
WORKDIR /srv/RK_LIMS/server
RUN pip3 install -r requirements.txt
RUN pip3 install mysqlclient-1.4.2-cp37-cp37m-win32.whl

# Configure printing requirements
COPY printers.conf /etc/cups/

# Open port 5000 for HTTP
EXPOSE 5000

#CMD ["/usr/sbin/cupsd", "-f"]
#CMD ["python3", "main.py", "--dbhost", "10.0.2.2"]
CMD service cups start && python3 app.py --dbhost 10.0.2.2