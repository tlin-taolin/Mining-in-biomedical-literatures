DEBUG=false
# run the command
cp ../phenotype_graph/data/ngram_name_tokens db/
sudo rm -rf db/tmp/
echo 64211130 | sudo -S docker exec crawl python '/home/tlin/notebooks/start.py'

# backup the result
if ! $DEBUG; then
    sudo docker exec mongodb bash -c 'mongodump --out=/data/tmp'
    tar -zcvf db/backup.tar.gz db/tmp
fi
