kubectl delete -f kubernetes/playlist/playlist.yaml
kubectl delete -f kubernetes/playlist/userservice.yaml
kubectl delete -f kubernetes/song/search.yaml
kubectl delete -f kubernetes/song/songcomments.yaml
kubectl delete -f kubernetes/song/songdetails.yaml
kubectl delete -f kubernetes/song/songservice.yaml
kubectl delete -f kubernetes/topchart/allcontentservice.yaml
kubectl delete -f kubernetes/topchart/topchart.yaml
kubectl delete -f kubernetes/db.yaml
kubectl delete -f kubernetes/hpa.yaml
kubectl delete -f kubernetes/ingress.yaml
kubectl delete -f kubernetes/podmonitoring.yaml
kubectl delete -f kubernetes/service.yaml

minikube stop
