############ Python based ############
parse_data:
	python parsing/parse_data.py
clean_data:
	python parsing/clean_data.py
extract_features:
	python parsing/extract_features.pys
analyze_phenotype_in_word2vec:
	python parsing/analyze_phenotype.py
preprocessing_pipeline:
	python parsing/parse_data.py
	python parsing/clean_data.py

######### Scala/Spark based #########
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
# analyze_features_in_spark:
