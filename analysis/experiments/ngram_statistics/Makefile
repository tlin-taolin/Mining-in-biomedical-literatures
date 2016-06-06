HOST=spark-m
G5K=reims

build_cluster:
	gcloud beta dataproc clusters create spark \
	--zone europe-west1-c --master-machine-type n1-standard-4 \
	--master-boot-disk-size 256 --num-workers 19 \
	--worker-machine-type n1-standard-4 \
	--worker-boot-disk-size 128 --image-version 1.0 \
	--initialization-actions gs://data_in_cloud/ipython.sh

destory_cluster:
	gcloud beta dataproc clusters delete spark

cp_data_gs:
	gsutil cp ipython.sh gs://data_in_cloud/

cp_data_cloud:
	gcloud compute copy-files ../../data/parsed_all/all_in_one ${HOST}:ngram/data/
	gcloud compute copy-files ../../data/hp/parsed_name ${HOST}:ngram/data/

cp_jar_cloud:
	sbt package
	gcloud compute copy-files target/scala-2.10/nlp-analysis_2.10-1.0.jar ${HOST}:ngram/
	gcloud compute copy-files Makefile ${HOST}:ngram/

cp_data_hdfs:
	hadoop fs -put data

ssh_tunnel:
	gcloud compute ssh  --zone=us-central1-c \
	  --ssh-flag="-D 1080" --ssh-flag="-N" --ssh-flag="-n" spark-m

configure_browser:
	/usr/bin/google-chrome \
	--proxy-server="socks5://localhost:1080" \
	--host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost" \
	--user-data-dir=/tmp/

run-cloud:
	hadoop fs -rm -r -f result
	spark-submit \
		--class NgramLevel \
		--master yarn \
		--deploy-mode client\
		--num-executors 25 \
		--executor-cores 3 \
		--driver-memory 8g \
		--executor-memory 8g \
		nlp-analysis_2.10-1.0.jar


cp_data_g5k:
	scp -r ../../data/parsed_all/all_in_one tlin@access.grid5000.fr:${G5K}/data/
	scp -r ../../data/hp/parsed_name tlin@access.grid5000.fr:${G5K}/data/

cp_code_g5k:
	sbt package
	scp target/scala-2.10/nlp-analysis_2.10-1.0.jar tlin@access.grid5000.fr:${G5K}/ngram/code/
	scp Makefile tlin@access.grid5000.fr:${G5K}/ngram/


cp_code_g5k_hdfs:
	hg5k --putindfs ../data .


run_code_g5k:
	  spark_g5k --scala_job code/nlp-analysis_2.10-1.0.jar \
				--main_class NgramLevel \
 			  	--exec_params \
				num-executors=40 \
				executor-cores=6 \
				executor-memory=8g \
				driver-memory=4g \
				driver-cores=4
