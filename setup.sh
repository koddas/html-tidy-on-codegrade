#!/bin/sh

pip3 install typer

chmod +x $FIXTURES/install-tidy.py
$FIXTURES/install-tidy.sh

# Makes the run script executable
chmod +x $FIXTURES/tidy.py
