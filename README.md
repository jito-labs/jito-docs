Jito Docs
=======================================

This repo contains Jito Labs documentation

## Installation

```
pip install sphinx
pip install -r ./docs/requirements.txt
```

## Build

```
cd ./jito-docs/docs
make clean
make html
firefox build/html/index.html
```

## CI
This automatically triggers Read the Docs to update that domain every time main has a merge. 

