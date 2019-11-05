@echo off

docker-compose build main
docker-compose run --rm main
