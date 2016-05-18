HOST=spark-m

build_cluster:
	gcloud beta dataproc clusters create spark \
	--zone us-central1-c --master-machine-type n1-standard-2 \
	--master-boot-disk-size 256 --num-workers 5 \
	--worker-machine-type n1-standard-4 \
	--worker-boot-disk-size 500 --image-version 1.0 \
	--project LabAuwerx

destory_cluster:
	gcloud beta dataproc clusters \
	delete spark \
	--project LabAuwerx

cp_data_cloud:
	gcloud compute copy-files ../data/parsed_all/all_in_one ${HOST}:data/
	gcloud compute copy-files ../data/graph/parsed_name ${HOST}:data/

cp_jar_cloud:
	sbt package
	gcloud compute copy-files target/scala-2.10/nlp-analysis_2.10-1.0.jar ${HOST}:
	gcloud compute copy-files Makefile ${HOST}:

run-cloud:
	hadoop fs -rm -r -f stat-score
	spark-submit \
		--class NgramMain \
		--num-executors 10 \
		--executor-cores 3 \
		--driver-memory 8g \
		--executor-memory 8g \
		nlp-analysis_2.10-1.0.jar


run-local:
	sbt package
	gcloud beta dataproc jobs submit spark \
		--cluster spark \
		--jars target/scala-2.10/nlp-analysis_2.10-1.0.jar \
		--class NgramMain \
		--num-executors 10 \
		--executor-cores 2 \
		--driver-memory 8g \
		--executor-memory 8g \
		5
