#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-jaeger -n jaeger bitnami/jaeger # -f jaeger-values.yaml
kubectl apply -f $BASEDIR/jaeger-nodeports.yaml -n jaeger

echo "Ждем готовности всех подов Jaeger в течение 10 минут..."

kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=my-jaeger -n jaeger --timeout=600s
