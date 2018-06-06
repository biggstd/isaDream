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

# Setup bokeh variables.
ENV BOKEH_RESOURCES=inline

COPY ./bokehtest /bokehtest
COPY ./NMRDemo /NMRDemo
COPY ./testvis /testvis

# Add entrypoint (this allows variable expansion)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
