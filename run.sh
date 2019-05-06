#!/usr/bin/env bash

MUSIC_DIR=/Users/jaivalis/Music/iTunes

docker run \
    -v ${MUSIC_DIR}:/music \
    -e PLAYER_ENDPOINT=http://jukepi-rest-player:8888 \
    --network=jukepi-network \
    -p 8080:8080 \
    --name jukepi \
    jukepi