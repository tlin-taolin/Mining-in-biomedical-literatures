DEBUG=false
# run the command
cp ../phenotype_graph/data/ngram_name_tokens db/
sudo rm -rf db/tmp/
docker exec crawl python '/home/tlin/notebooks/start.py'

# backup the result
if ! $DEBUG; then
    docker exec mongodb bash -c 'mongodump --out=/data/tmp'
    tar -zcvf db/backup.tar.gz db/tmp
fi
