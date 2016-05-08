############ Python based ############
parse_data:
	python parsing/parse_data.py
clean_data:
	python parsing/clean_data.py
preprocessing_pipeline:
	python parsing/parse_data.py
	python parsing/clean_data.py
extract_doc_feature:
	python parsing/extract_doc_feature.py
calculate_word2vec_distance_of_phenotype:
	python parsing/calculate_word2vec_distance_of_phenotype.py
extract_relationship_of_phenotype:
	python parsing/extract_relationship_phenotype.py
analyze_pipeline:
	python parsing/calculate_word2vec_distance_of_phenotype.py
	python parsing/extract_relationship_phenotype.py

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
