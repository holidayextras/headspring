# source image

#only run locally -- possible more to do w.r.t. deploy
#but we're building locally so the image will get built here!
first build base image with

cd acacia
docker build -t acacia acacia/

# headspring
generic-ish python source API

# deploy to GCP

# build the image:

docker build -t gcr.io/hx-test/source-master .

# push to gcr.io:

gcloud docker push gcr.io/hx-test/source-master

# create the cluster (note the scope):

gcloud container clusters create NAME --num-nodes 1 --machine-type g1-small --scopes https://www.googleapis.com/auth/cloud-platform

# create the pod:

kubectl run NAME --image=gcr.io/hx-test/source-master --port=8080

# expose port 8080 to the outside world:

kubectl expose rc NAME --type="LoadBalancer"

# list the IP address the pod is listening on (this will take a few minutes to allocate the external IP):

kubectl get services NAME

For more verbose information (incl errors):

kubectl describe services/NAME

# curl some stuff to it:

curl -X POST -H "Content-Type:application/json" -d '{"name":"bears","tags" : [ "stuff", "more stuff" ]}' [external IP]:8080/post
