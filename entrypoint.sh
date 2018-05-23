#!/usr/bin/env bash
bokeh serve --port ${PORT}\
  --use-xheaders\
  --address 0.0.0.0\
  --allow-websocket-origin ${ORIGIN}\
  --log-level ${LOG_LEVEL}\
  /bokehtest\
  /testvis\
