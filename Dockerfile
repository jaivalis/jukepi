FROM alpine:3.8

ADD jukepi/ /jukepi
ADD library_updater.py /
ADD requirements.txt /
ADD resources /resources
ADD templates /templates
ADD static /static

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