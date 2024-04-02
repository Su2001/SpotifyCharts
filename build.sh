#DOCKER_BUILDKIT=1 docker build . -f playlist/Dockerfile -t playlist 
#DOCKER_BUILDKIT=1 docker build . -f userService/Dockerfile -t userservice 
DOCKER_BUILDKIT=1 docker build . -f songComments/Dockerfile -t songcomments 
DOCKER_BUILDKIT=1 docker build . -f songService/Dockerfile -t songservice 

docker-compose up