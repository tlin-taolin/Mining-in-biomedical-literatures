sudo docker rm -f `sudo docker ps -aq`
sudo docker run -v "$(pwd)"/data:/data --name mongodb -d mongo mongod --smallfiles
sudo docker run -it --name crawl -v "$(pwd)":/home/tlin/notebooks --link mongodb:mongodb itamtao/scrapy-mongo zsh
