build:
	./.build.sh
run:
	./.run.sh
backup_host:
	sudo docker exec mongodb bash -c 'mongodump --out=/data/tmp/'
	tar -zcvf db/backup.tar.gz db/tmp/*
	sudo rm -rf db/tmp/
restore_host:
	sudo docker exec mongodb bash -c 'mkdir -p /data/tmp; tar xv -C /data/tmp -f /data/backup.tar.gz'
	sudo docker exec mongodb bash -c 'mongorestore --db crawl /data/tmp/db/tmp/crawl'
	sudo rm -rf db/tmp/
