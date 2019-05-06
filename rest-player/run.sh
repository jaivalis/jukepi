#!/usr/bin/env bash


docker network create -d bridge mybridge
docker rm $(docker ps -a -q)

MUSIC_DIR=/Users/jaivalis/Music/iTunes

docker run \
    -v ${MUSIC_DIR}:/music \
    -e PLAYER=mock \
    --network=mybridge \
    -p 8888:8888 \
    --name jukepi-rest-player \
    jukepi-rest-player
