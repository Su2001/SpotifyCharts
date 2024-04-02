DOCKER_BUILDKIT=1 docker build . -f playlist/Dockerfile -t playlist 
DOCKER_BUILDKIT=1 docker build . -f userService/Dockerfile -t userservice 
DOCKER_BUILDKIT=1 docker build . -f songComments/Dockerfile -t songcomments 
DOCKER_BUILDKIT=1 docker build . -f songService/Dockerfile -t songservice

DOCKER_BUILDKIT=1 docker build . -f search/Dockerfile -t searchservice 
DOCKER_BUILDKIT=1 docker build . -f allContent/Dockerfile -t allcontentservice 
DOCKER_BUILDKIT=1 docker build . -f topCharts/Dockerfile -t topchartsservice
DOCKER_BUILDKIT=1 docker build . -f songDetails/Dockerfile -t songdetailsservice  

docker-compose up