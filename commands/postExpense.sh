#!/bin/bash

token=12345678

curl --data "token=$token&amount=$1&text=$2" http://localhost:8008/submit/expense/ 