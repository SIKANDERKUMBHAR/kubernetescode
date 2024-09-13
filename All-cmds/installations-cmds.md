
# Installation Guide for Jenkins, Docker, Kubernetes, Kind, ArgoCD, and Kubernetes Dashboard

## Overview
This guide provides detailed instructions to install Jenkins, Docker, Kubernetes CLI (`kubectl`), Kind, ArgoCD, and the Kubernetes Dashboard on a Linux system. These tools are essential for setting up a CI/CD pipeline for deploying applications to Kubernetes clusters.

### Prerequisites
- Linux system (preferably Ubuntu/Debian-based).
- Administrative privileges (sudo access).

## Step 1: Update System and Install Dependencies

### 1.1 Update Package List
```bash
sudo apt update -y
```

### 1.2 Install Java (Required for Jenkins)
```bash
sudo apt install openjdk-11-jdk -y
```

### 1.3 Install Docker (Required for Kubernetes/Minikube)
```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
sudo usermod -aG docker jenkins
sudo chown ubuntu:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
```

## Step 2: Install Jenkins

### 2.1 Add Jenkins Repository Key and Source
```bash
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

### 2.2 Install Jenkins
```bash
sudo apt-get update
sudo apt-get install jenkins -y
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo usermod -aG docker jenkins
```

## Step 3: Install AWS CLI

```bash
sudo apt install awscli -y
```

## Step 4: Install Kubernetes CLI (`kubectl`)

### 4.1 Install `kubectl`
```bash
VERSION="v1.30.0"
URL="https://dl.k8s.io/release/${VERSION}/bin/linux/amd64/kubectl"
curl -LO "$URL"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

## Step 5: Install Kind (Kubernetes in Docker)

### 5.1 Install Kind for AMD64/x86_64
```bash
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo cp ./kind /usr/local/bin/kind
rm -rf kind
```

## Step 6: Create a Kubernetes Cluster Using Kind

### 6.1 Define Cluster Configuration (`config.yml`)
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  image: kindest/node:v1.30.0
- role: worker
  image: kindest/node:v1.30.0
- role: worker
  image: kindest/node:v1.30.0
```

### 6.2 Create Kind Cluster
```bash
kind create cluster --config=config.yml
kubectl cluster-info --context kind-kind
kubectl get nodes
kind get clusters
```

## Step 7: Install and Configure ArgoCD

### 7.1 Install ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 7.2 Verify ArgoCD Installation
```bash
kubectl get svc -n argocd
```

### 7.3 Change ArgoCD Service Type to NodePort
```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
```

### 7.4 Access ArgoCD UI
Forward ports to access the ArgoCD server UI:
```bash
kubectl port-forward svc/argocd-server -n argocd 8081:80 8443:443 --address=0.0.0.0
```

### 7.5 Retrieve ArgoCD Admin Password
```bash
kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```

## Step 8: Install Kubernetes Dashboard

### 8.1 Create Service Account and Cluster Role Binding (`dashboard.yml`)
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

### 8.2 Deploy Kubernetes Dashboard
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

### 8.3 Create Token for Dashboard Access
```bash
kubectl -n kubernetes-dashboard create token admin-user
```

### 8.4 Access Kubernetes Dashboard
```bash
kubectl port-forward svc/kubernetes-dashboard -n kubernetes-dashboard 31577:443 --address=0.0.0.0
```

## Step 9: Access Deployed Application

To access the Flask application deployed on Kubernetes (exposed via ArgoCD), run:
```bash
kubectl port-forward service/flaskdemo-service 30001:80 --address=0.0.0.0 -n argocd
```

## Conclusion

This guide provides a comprehensive setup for deploying a CI/CD environment using Jenkins, Docker, Kubernetes, Kind, and ArgoCD. By following these steps, you can set up a complete pipeline to build, test, and deploy your application to Kubernetes.