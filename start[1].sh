#!/bin/bash

rasa run actions &

sleep 10

rasa run \
  --enable-api \
  --cors "*" \
  --credentials credentials.yml \
  --port 7860