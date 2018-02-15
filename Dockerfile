FROM ubuntu:16.04

LABEL maintainer='makopov@pnnl.gov'

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN python3.6 -m pip install bokeh pandas isatools

RUN mkdir /opt/isadream

COPY . /opt/isadream/

WORKDIR /opt/isadream

EXPOSE 5006

CMD ["bokeh", "serve", "NMRDemo/", "--allow-websocket-origin=localhost:8001"]