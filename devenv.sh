#!/bin/sh 
tmux new-window 'pypy3 envri.py'
tmux new-window 
tmux split-window -h 'mongo 127.0.0.1:27017/HakureiShop'
tmux split-window -v 'bpython'
tmux select-pane -R
tmux next-window
tmux kill-window

