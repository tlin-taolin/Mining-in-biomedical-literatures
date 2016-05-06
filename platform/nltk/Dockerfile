FROM itamtao/scipy-dev

MAINTAINER Tao Lin <itamtao@gmail.com>

RUN pip install -U nltk

# COPY nltk-install-all-data.sh /tmp/
# RUN sh /tmp/nltk-install-all-data.sh

# Install requirements.
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt


# switch user
USER tlin
VOLUME /home/tlin/notebooks
VOLUME /nltk
WORKDIR /home/tlin/notebooks

RUN git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh \
      && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
