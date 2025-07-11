#!/bin/bash
python3 -m nuitka --clang --standalone --onefile --output-filename=floor-browse --enable-plugin=tk-inter --include-package=lupa src/main.py