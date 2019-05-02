#!/usr/bin/env bash

# --device /dev/snd works on linux
#docker run \
#    -v /Users/jaivalis/Music/iTunes:/Users/jaivalis/Music/iTunes \
#    -p 8080:8080/tcp \
#    --device /dev/snd \
#    --name jukepi \
#    jukepi

docker run \
    -v /Users/jaivalis/Music/iTunes:/Users/jaivalis/Music/iTunes \
    --network=host \
    --name jukepi \
    jukepi
#    --network jukepi-network \
#    -p 8080:8080/tcp \


#docker run -ti \
#    -v /Users/jaivalis/Music/iTunes:/Users/jaivalis/Music/iTunes \
#    -p 8080:8080/tcp \
#    --name jukepi \
#    jukepi bash