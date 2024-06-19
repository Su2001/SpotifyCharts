kubectl delete -f kubernetes/playlist/playlist.yaml
kubectl delete -f kubernetes/playlist/userservice.yaml
kubectl delete -f kubernetes/song/search.yaml
kubectl delete -f kubernetes/song/songcomments.yaml
kubectl delete -f kubernetes/song/songdetails.yaml
kubectl delete -f kubernetes/song/songservice.yaml
kubectl delete -f kubernetes/topchart/allcontentservice.yaml
kubectl delete -f kubernetes/topchart/topchart.yaml
kubectl delete -f kubernetes/ingress.yaml
kubectl delete -f kubernetes/config-map.yaml
kubectl delete -f kubernetes/secret.yaml
kubectl delete -f prometheus/components.yaml
kubectl create configmap prometheus-cm --from-file prometheus-cm.yaml
kubectl delete -f prometheus/grafana.yaml
kubectl delete svc,deploy,pod --all



