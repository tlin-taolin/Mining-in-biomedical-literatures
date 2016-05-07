docker rm -f `docker ps -aq`
docker run -v "$(pwd)"/data:/data --name mongodb -d mongo mongod --smallfiles
docker run -it --name crawl -v "$(pwd)":/home/tlin/notebooks --link mongodb:mongodb itamtao/scrapy-mongo zsh
