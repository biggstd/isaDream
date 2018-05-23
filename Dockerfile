FROM python:3.6-stretch

# Install nodejs (see: https://askubuntu.com/a/720814)
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash \
    && apt-get install nodejs \
    && apt-get -yq autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install --pre -i https://pypi.anaconda.org/bokeh/channel/dev/simple\
    --extra-index-url https://pypi.python.org/simple/\
    bokeh\
    pandas\
    isatools\
    && rm -rf ~/.cache/pip


RUN mkdir /opt/isadream
COPY . /opt/isadream/
WORKDIR /opt/isadream/
RUN python setup.py install



ENV ORIGIN="idreamvisualization.pnl.gov:8123" \
    PORT="5006" \
    LOG_LEVEL="info" \
    BOKEH_RESOURCES="inline"


COPY ./bokehtest /bokehtest
COPY ./NMRDemo /NMRDemo
COPY ./testvis /testvis

# Add entrypoint (this allows variable expansion)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]







# FROM ubuntu:16.04
#
# LABEL maintainer='makopov@pnnl.gov'
#
# RUN apt-get update
# RUN apt-get install -y software-properties-common vim
# RUN add-apt-repository ppa:jonathonf/python-3.6
# RUN apt-get update
#
# # Prepare a Python 3.6 installation.
# RUN apt-get install -y\
#   build-essential\
#   python3.6\
#   python3.6-dev\
#   python3-pip\
#   python3.6-venv
#   # python3.6-distutils
#
# # Install git.
# RUN apt-get install -y git
#
# # update pip
# RUN python3.6 -m pip install pip --upgrade
# RUN python3.6 -m pip install wheel
# RUN python3.6 -m pip install bokeh pandas isatools
#
# RUN mkdir /opt/isadream
#
# COPY . /opt/isadream/
#
# # Set acceptable connection sources.
# ENV BOKEH_ALLOWED_WEBSOCKET="localhost/idreamvisualization.pnl.gov"
# # Replace URL in bokeh service
# # RUN sed -i -e 's/localhost:8001/idreamvisualization\.pnl\.gov/g' /opt/isadream/dockerbokeh.py
#
# WORKDIR /opt/isadream
#
# EXPOSE 5006
#
# # Set the bokeh server log level.
# ENV BOKEH_PY_LOG_LEVELL=debug
#
# # CMD ["python3.6", "dockerbokeh.py", "$>bokeh_server.log"]
# CMD ["bokeh", "serve", "--show", "--port=5006",\
#      "--allow-websocket-origin=${BOKEH_ALLOWED_WEBSOCKET}"]
