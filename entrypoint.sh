#!/usr/bin/env bash
bokeh serve --port ${PORT}\
  --use-xheaders\
  --address 0.0.0.0\
  --allow-websocket-origin 0.0.0.0\
  --allow-websocket-origin localhost\
  --allow-websocket-origin idreamvisualization.pnl.gov\
  --log-level ${LOG_LEVEL}\
  /bokehtest\
  /testvis\
