FROM itamtao/scrapy

MAINTAINER Tao Lin <itamtao@gmail.com>

USER root

# Install requirements.
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

USER tlin
