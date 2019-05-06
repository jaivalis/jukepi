#!/usr/bin/env bash


docker run \
    -v /Users/jaivalis/Music/iTunes:/Users/jaivalis/Music/iTunes \
    --network=mybridge \
    -p 8080:8080 \
    --name jukepi \
    jukepi