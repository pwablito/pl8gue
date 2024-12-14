# Pl8gue
Kubernetes application for pl8guing your cluster

## Build
```sh
docker build -t $REPO:$VERSION app
docker push $REPO:$VERSION
```

## Install
```sh
helm install --create-namespace --namespace $NAMESPACE $RELEASE_NAME ./helm
```