#!/bin/bash

python ../manage.py shell << EOF
from users.models import *
init_model()
EOF