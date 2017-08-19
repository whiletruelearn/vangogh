#!/bin/bash

easy_install virtualenv

virtualenv ./vangogh

source ./vangogh/bin/activate

pip install http://download.pytorch.org/whl/cu75/torch-0.2.0.post1-cp27-cp27m-manylinux1_x86_64.whl 
pip install torchvision 

pip install -r requirements.txt
export PYTHONPATH=./
python api/api.sh
