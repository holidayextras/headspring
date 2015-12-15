#!/bin/bash

#  build the base image
docker build -t acacia acacia/

#  build the application image
docker build -t gcr.io/hx-test/source-master-cidev .

#  push the application image to gcr
/opt/google-cloud-sdk/bin/gcloud docker push gcr.io/hx-test/source-master-cidev
