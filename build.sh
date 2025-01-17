#minikube start
#minikube addons enable metrics-server
kubectl create -f kubernetes/secret.yaml
kubectl create -f kubernetes/config-map.yaml
kubectl apply -f kubernetes/playlist/playlist.yaml
kubectl apply -f kubernetes/playlist/userservice.yaml

kubectl apply -f kubernetes/song/search.yaml
kubectl apply -f kubernetes/song/songcomments.yaml
kubectl apply -f kubernetes/song/songdetails.yaml
kubectl apply -f kubernetes/song/songservice.yaml

kubectl apply -f kubernetes/topchart/allcontentservice.yaml
kubectl apply -f kubernetes/topchart/topchart.yaml
kubectl apply -f kubernetes/ingress.yaml

kubectl apply -f prometheus/components.yaml

kubectl create configmap prometheus-cm --from-file prometheus/prometheus-cm.yaml
kubectl apply -f prometheus/prometheus.yaml
kubectl apply -f prometheus/grafana.yaml
kubectl port-forward service/grafana-svc 4200:3000

#kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml

# DOCKER_BUILDKIT=1 docker build . -f playlist/Dockerfile -t playlist 
# DOCKER_BUILDKIT=1 docker build . -f userService/Dockerfile -t userservice 
# DOCKER_BUILDKIT=1 docker build . -f songComments/Dockerfile -t songcomments 
# DOCKER_BUILDKIT=1 docker build . -f songService/Dockerfile -t songservice

# DOCKER_BUILDKIT=1 docker build . -f search/Dockerfile -t searchservice 
# DOCKER_BUILDKIT=1 docker build . -f allContent/Dockerfile -t allcontentservice 
# DOCKER_BUILDKIT=1 docker build . -f topCharts/Dockerfile -t topchartsservice
# DOCKER_BUILDKIT=1 docker build . -f songDetails/Dockerfile -t songdetailsservice  

# docker-compose  up