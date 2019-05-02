#!/usr/bin/env bash


#docker rm $(docker ps -a -q)

MUSIC_DIR=/Users/jaivalis/Music/iTunes

docker run \
    -v ${MUSIC_DIR}:/music \
    -e PLAYER=mock \
    --network="host" \
    --name jukepi-rest-player \
    jukepi-rest-player
#     --network jukepi-network \
#    -p 8888:8888 \
