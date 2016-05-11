HOST=hpc-8
# CODE=analysis
CODE=data_crawler


start_cloud:
	gcloud compute instances start ${HOST}

cp_cloud:
	gcloud compute copy-files ../../textmining ${HOST}:/datadisk/
	gcloud compute ssh ${HOST}

cp_code:
	gcloud compute copy-files ${CODE}/ ${HOST}:/datadisk/textmining/code/

close_cloud:
	gcloud compute instances stop ${HOST}

