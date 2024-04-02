DOCKER_BUILDKIT=1 docker build . -f playlist/Dockerfile -t playlist 
DOCKER_BUILDKIT=1 docker build . -f userService/Dockerfile -t recommendations 

docker-compose up