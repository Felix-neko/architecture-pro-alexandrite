#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

kubectl create namespace web-services
kubectl apply -f $BASEDIR/nginx-stateful-nodeport.yaml -n web-services

kubectl create namespace logging

helm repo add elastic https://helm.elastic.co
helm repo update

helm install elasticsearch elastic/elasticsearch -n logging \
  --set replicas=1 \
  --set resources.requests.memory=2Gi \
  --set esConfig."elasticsearch\.yml"="xpack.security.enabled: false"

helm install kibana elastic/kibana -n logging \
  --set service.type=ClusterIP

helm install filebeat elastic/filebeat -n logging -f $BASEDIR/filebeat-values.yaml