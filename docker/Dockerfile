#############################
### Build DataPusher Plus ###
#############################
FROM ubuntu:jammy

LABEL maintainer="Texas Natural Resources Information Systems <tnris.twdb@gmail.com>"
LABEL org.opencontainers.image.source https://github.com/ctrepka/docker-datapusher-plus


# Set CKAN version to build
ENV GIT_URL=https://github.com/ckan/ckan.git
ENV GIT_BRANCH=ckan-2.9.5

# Set timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set Locale
ENV LC_ALL=en_US.UTF-8

ENV SRC_DIR=/srv/app/src
ENV VENV=/usr/lib/ckan/datapusher-plus
ENV DATAPUSHER_CFG_DIR=/etc/ckan/datapusher

WORKDIR ${SRC_DIR}

# Set the locale          
RUN apt-get update
RUN apt-get install --no-install-recommends -y locales
RUN sed -i "/$LC_ALL/s/^# //g" /etc/locale.gen
RUN dpkg-reconfigure --frontend=noninteractive locales 
RUN update-locale LANG=${LC_ALL}

# Instal apt-utils
RUN apt-get install --no-install-recommends -y \
    apt-utils \
    python3-venv \
    python3-dev \
    python3 \
    build-essential \
    libxslt1-dev \
    libxml2-dev \
    libffi-dev \
    wget \
    curl \
    unzip \
    python3-pip \
    git


RUN wget https://github.com/jqnatividad/qsv/releases/download/0.46.1/qsv-0.46.1-x86_64-unknown-linux-gnu.zip
RUN unzip qsv-0.46.1-x86_64-unknown-linux-gnu.zip
RUN mv qsvdp /usr/local/bin && ls -la
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN python -m venv ${VENV}
#RUN ${VENV}/bin/pip install datapusher-plus uwsgi #
RUN ${VENV}/bin/pip install uwsgi
## CLONING HOTFIX BRANCH FROM TWDBBEN
RUN git clone --single-branch --branch hotfix https://github.com/twdbben/datapusher-plus.git
RUN cd ${SRC_DIR}/datapusher-plus && \
    ${VENV}/bin/pip install -r requirements-dev.txt && \
    ${VENV}/bin/pip install -e .


RUN mkdir -p ${DATAPUSHER_CFG_DIR}
# USING CONFIG FILES FROM TWDBEN HOTFIX FORK/BRANCH
RUN curl https://raw.githubusercontent.com/twdbben/datapusher-plus/hotfix/datapusher/settings.py -o ${DATAPUSHER_CFG_DIR}/settings.py
RUN curl https://raw.githubusercontent.com/twdbben/datapusher-plus/hotfix/deployment/datapusher-uwsgi.ini -o ${DATAPUSHER_CFG_DIR}/uwsgi.ini

ENV JOB_CONFIG=${DATAPUSHER_CFG_DIR}/settings.py

ENTRYPOINT ${VENV}/bin/datapusher_initdb ${DATAPUSHER_CFG_DIR}/settings.py && ${VENV}/bin/uwsgi --enable-threads -i ${DATAPUSHER_CFG_DIR}/uwsgi.ini

EXPOSE 8800