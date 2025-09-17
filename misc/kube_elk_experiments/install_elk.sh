#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

kubectl create namespace web-services
kubectl apply -f $BASEDIR/nginx-stateful-nodeport.yaml -n web-services

kubectl create namespace logging

helm repo add elastic https://helm.elastic.co
helm repo update

helm install elasticsearch elastic/elasticsearch -n logging -f $BASEDIR/elasticsearch-values.yaml

helm install kibana elastic/kibana -n logging -f $BASEDIR/kibana-values.yaml

helm install filebeat elastic/filebeat -n logging -f $BASEDIR/filebeat-values.yaml

kubectl apply -f $BASEDIR/kibana-nodeport.yaml -n logging