# IS_DB="$(sudo docker ps -aq --filter 'name=mongodb')"
#
# if [ $IS_DB ]; then
#     sudo docker exec mongodb bash -c 'mongodump --out=/data/tmp'
#     tar -zcvf db/backup.tar.gz /tmp
# fi
docker rm -f `docker ps -aq`
docker run -v "$(pwd)"/db:/data --name mongodb -d mongo mongod --smallfiles
docker run --rm -it --name crawl -v "$(pwd)":/home/tlin/notebooks --link mongodb:mongodb itamtao/scrapy-mongo zsh
