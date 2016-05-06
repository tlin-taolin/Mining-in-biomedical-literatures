rm -rf data/raw
mkdir -p data/raw
tar xv -C data/raw -f ../data_crawler/db/backup.tar.gz
mv data/raw/db/tmp/crawl/* data/raw/
rm -rf data/raw/db
echo 64211130 | sudo -S docker rm -f `sudo docker ps -aq`
sudo docker run -it -v "$(pwd)":/home/ --name mongodb -d mongo
sudo docker exec mongodb bash -c 'bsondump /home/data/raw/pmcdoc.bson > /home/data/raw/pmcdoc.json'
