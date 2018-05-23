#!/usr/bin/env bash
bokeh serve --port ${PORT}\
  --use-xheaders\
  --address idreamvisualization.pnl.gov\
  --allow-websocket-origin ${ORIGIN}\
  --log-level ${LOG_LEVEL}\
  /bokehtest\
  /testvis\
