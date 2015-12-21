#!/bin/bash

#  build the base image
docker build -t acacia acacia/
ret_val=$?

if [ $ret_val -eq 0 ]; then
  #  build the application image
  docker build -t gcr.io/hx-test/source-master-cidev .
  ret_val=$?
fi

if [ $ret_val -eq 0 ]; then
  #  push the application image to gcr
  /opt/google-cloud-sdk/bin/gcloud docker push gcr.io/hx-test/source-master-cidev
  ret_val=$?
fi 

exit $ret_val
