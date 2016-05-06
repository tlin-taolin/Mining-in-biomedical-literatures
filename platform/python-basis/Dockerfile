FROM buildpack-deps:trusty

# Inspired by [ruimashita/dockerfiles](https://github.com/ruimashita/dockerfiles)

MAINTAINER Tao Lin <itamtao@gmail.com>

# faster apt source
RUN echo "deb mirror://mirrors.ubuntu.com/mirrors.txt trusty main restricted universe multiverse \n\
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-updates main restricted universe multiverse \n\
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-backports main restricted universe multiverse \n\
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-security main restricted universe multiverse" > /etc/apt/sources.list

# install some necessary ....
RUN apt-get update && apt-get install -y zsh
RUN apt-get install -y git
RUN apt-get install libfreetype6-dev

# add new user: tlin
RUN useradd --create-home --shell /bin/zsh tlin
RUN git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh \
      && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc \
      && chsh -s /bin/zsh

# intall python
RUN apt-get install -y --no-install-recommends \
    python \
    python-dev

# install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && rm get-pip.py

# Fix: InsecurePlatformWarning
# http://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && pip install --no-cache-dir ndg-httpsclient

# set environments
RUN apt-get -qq install language-pack-en
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV PYTHONIOENCODING UTF-8
