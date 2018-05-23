#!/usr/bin/env bash
bokeh serve\
  --port 5006\
  --use-xheaders\
  --address 0.0.0.0\
  --allow-websocket-origin 0.0.0.0\
  --allow-websocket-origin localhost\
  --allow-websocket-origin idreamvisualization.pnl.gov\
  --log-level debug\
  /bokehtest\
  /testvis\
