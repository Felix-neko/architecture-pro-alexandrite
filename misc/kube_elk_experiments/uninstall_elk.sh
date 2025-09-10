#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

kubectl delete namespace logging
kubectl delete namespace web-services