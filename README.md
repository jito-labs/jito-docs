[![Documentation Status](https://readthedocs.org/projects/jito-docs/badge/?version=latest)](https://jito-docs.readthedocs.io/en/latest/?badge=latest)
![Version](https://img.shields.io/badge/version-0.1.0-blue)


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

