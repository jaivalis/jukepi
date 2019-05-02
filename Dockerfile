#FROM centos:7
#
#ADD jukepi/ /jukepi
#ADD library_updater.py /
#ADD requirements.txt /
#ADD resources /resources
#
#
## install python
##RUN yum -y install epel-release && yum clean all
##RUN yum -y install python-pip && yum clean all
#RUN yum -y install gcc openssl-devel bzip2-devel libffi-devel
#RUN curl -L https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz | tar zx
#RUN cd Python-3.7.3
#RUN ./configure --enable-optimizations
#
## install vlc media player
#RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm
#RUN rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
#RUN yum -y install vlc && yum clean all
#
#
#CMD [ "pip3", "install", "-r", "requirements" ]
#
#CMD [ "python", ".library_updater.py" ]
#CMD [ "python", "-m", "jukepi.ui.server" ]

FROM alpine:3.8

ADD jukepi/ /jukepi
ADD library_updater.py /
ADD requirements.txt /
ADD resources /resources

# Update & Install dependencies
RUN apk add --no-cache --update \
    git \
    bash \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    build-base
RUN apk add linux-headers


# Set Python version
ARG PYTHON_VERSION='3.7.0'
# Set pyenv home
ARG PYENV_HOME=/root/.pyenv

# Install pyenv, then install python versions
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_HOME && \
    rm -rfv $PYENV_HOME/.git

ENV PATH $PYENV_HOME/shims:$PYENV_HOME/bin:$PATH

RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION
RUN pip install --upgrade pip && pyenv rehash
RUN pip install -r requirements.txt


## install vlc
#RUN apk add vlc
#RUN sed -i 's/geteuid/getppid/' /usr/bin/vlc

# Clean
RUN rm -rf ~/.cache/pip

EXPOSE 8080

CMD [ "python", ".library_updater.py" ]
CMD [ "python", "-m", "jukepi.ui.server" ]