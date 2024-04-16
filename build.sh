minikube start

kubectl apply -f kubernetes/playlist/playlist.yaml
kubectl apply -f kubernetes/playlist/userservice.yaml

kubectl apply -f kubernetes/song/search.yaml
kubectl apply -f kubernetes/song/songcomments.yaml
kubectl apply -f kubernetes/song/songdetails.yaml
kubectl apply -f kubernetes/song/songservice.yaml

kubectl apply -f kubernetes/topchart/allcontentservice.yaml
kubectl apply -f kubernetes/topchart/topchart.yaml

kubectl apply -f kubernetes/db.yaml
kubectl apply -f kubernetes/hpa.yaml
kubectl apply -f kubernetes/ingress.yaml
kubectl apply -f kubernetes/podmonitoring.yaml
kubectl apply -f kubernetes/service.yaml