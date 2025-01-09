#!/bin/bash

# Script para verificar o uso de disco de um PVC em um cluster Kubernetes

KUBECONFIG_PATH="$HOME/.kube/k8s-dev-op.yaml"
PVC_ID="pvc-97266b4c-f471-45b4-8fc3-f6644106d3ad"
KUBELET_PATH="/var/lib/kubelet/pods"

# Função para identificar o namespace e o pod que está utilizando o PVC
function find_pod_using_pvc() {
    echo "Procurando por pods que utilizam o PVC $PVC_ID..."

    # Listar todos os pods e namespaces
    PODS_INFO=$(kubectl --kubeconfig=$KUBECONFIG_PATH get pods --all-namespaces -o json)

    # Filtrar pods que utilizam o PVC específico
    POD_NAME=$(echo "$PODS_INFO" | jq -r ".items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName == \"$PVC_ID\") | .metadata.name")
    NAMESPACE=$(echo "$PODS_INFO" | jq -r ".items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName == \"$PVC_ID\") | .metadata.namespace")

    if [[ -z "$POD_NAME" ]]; then
        echo "Nenhum pod encontrado utilizando o PVC $PVC_ID."
        exit 1
    else
        echo "Pod encontrado: $POD_NAME no namespace: $NAMESPACE"
    fi
}

# Função para verificar o uso de disco no pod
function check_disk_usage_in_pod() {
    echo "Verificando o uso de disco no pod $POD_NAME..."

    # Executar comando df dentro do pod para verificar o uso de disco
    kubectl --kubeconfig=$KUBECONFIG_PATH exec -n $NAMESPACE $POD_NAME -- df -h | grep "$KUBELET_PATH/$POD_NAME/volumes/kubernetes.io~csi/$PVC_ID/mount"
}

# Main
find_pod_using_pvc
check_disk_usage_in_pod

