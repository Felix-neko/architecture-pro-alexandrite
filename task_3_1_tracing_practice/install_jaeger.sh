#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

#helm repo add bitnami https://charts.bitnami.com/bitnami
#helm repo update
helm install my-jaeger -n jaeger bitnami/jaeger -f jaeger-values.yaml