FROM ladybugtools/honeybee-radiance:1.66.42 as base

WORKDIR /home/ladybugbot/app
COPY . .

USER root

RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6 curl unzip -y \
    && pip3 install -r requirements.txt \
    && chown -R ladybugbot /home/ladybugbot/app

USER ladybugbot
