#!/usr/bin/env bash
bokeh serve\
  --port 5006\
  --use-xheaders\
  --address 0.0.0.0\
  --allow-websocket-origin 0.0.0.0\
  --allow-websocket-origin localhost:8123\
  --allow-websocket-origin idreamvisualization.pnl.gov\
  --allow-websocket-origin lampdev02.pnl.gov:8123\
  --log-level debug\
  /bokehtest\
  /testvis\
