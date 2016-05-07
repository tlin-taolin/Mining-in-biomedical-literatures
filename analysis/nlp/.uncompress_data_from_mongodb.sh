rm -rf data/raw
mkdir -p data/raw
tar xv -C data/raw -f ../../data_crawler/db/backup.tar.gz
mv data/raw/db/tmp/crawl/* data/raw/
rm -rf data/raw/db
docker rm -f `docker ps -aq`
docker run -it -v "$(pwd)":/home/ --name mongodb -d mongo
docker exec mongodb bash -c 'bsondump /home/data/raw/pmcdoc.bson > /home/data/raw/pmcdoc.json'
