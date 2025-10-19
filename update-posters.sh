#!/bin/bash
#
# Simple wrapper script to update the posters.md file
#
# This script runs the Python script to regenerate content/posters.md
# based on the images found in static/images/posters/
#

cd "$(dirname "$0")"
python3 update-posters.py
