DOCKER_BUILDKIT=1 docker build . -f playlist/Dockerfile -t playlist 
DOCKER_BUILDKIT=1 docker build . -f userService/Dockerfile -t userservice 
DOCKER_BUILDKIT=1 docker build . -f songComments/Dockerfile -t songcomments 
DOCKER_BUILDKIT=1 docker build . -f songService/Dockerfile -t songservice

DOCKER_BUILDKIT=1 docker build . -f search/Dockerfile -t searchservice 
DOCKER_BUILDKIT=1 docker build . -f allContent/Dockerfile -t allcontentservice 
DOCKER_BUILDKIT=1 docker build . -f topCharts/Dockerfile -t topchartsservice
DOCKER_BUILDKIT=1 docker build . -f songDetails/Dockerfile -t songdetailsservice  

docker tag playlist su2001/playlist
docker tag allcontentservice  su2001/allcontentservice 
docker tag userservice su2001/userservice 
docker tag songcomments su2001/songcomments
docker tag songservice su2001/songservice
docker tag searchservice su2001/searchservice
docker tag topchartsservice su2001/topchartsservice
docker tag songdetailsservice su2001/songdetailsservice

docker push su2001/playlist
docker push su2001/allcontentservice 
docker push su2001/userservice 
docker push su2001/songcomments
docker push su2001/songservice
docker push su2001/searchservice
docker push su2001/topchartsservice
docker push su2001/songdetailsservice