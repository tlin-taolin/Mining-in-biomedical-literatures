uncompress_data:
	sh .uncompress_data_from_mongodb.sh
build_nltk_platfrom:
	sh .build_nltk.sh
parse_data:
	python parsing/parse_data.py
clean_data:
	python parsing/clean_data.py
extract_features:
	python parsing/extract_features.py
analyze_features:
	python extraction/extract_features.py
preprocessing_pipeline:
	python parsing/parse_data.py
	python parsing/clean_data.py

build_spark_platfrom:
	sh .build_spark.sh
build_notebook:
	sh .build_notebook.sh
extract_features_spark:
	cd analysis && sbt package
	cd ../
	spark-submit \
	--class "Extraction" \
	--master yarn-client \
	--driver-memory 1g \
	--executor-memory 1g \
	--executor-cores 1 \
	analysis/target/scala-2.10/nlp-analysis_2.10-1.0.jar
analyze_features_spark:
	python extraction/extract_features.py
