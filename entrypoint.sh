#!/bin/sh
bokeh serve --port ${PORT}\
  --address 0.0.0.0\
  --allow-websocket-origin ${ORIGIN}\
  --log-level ${LOG_LEVEL}\
  /bokehtest\
  /testvis\
