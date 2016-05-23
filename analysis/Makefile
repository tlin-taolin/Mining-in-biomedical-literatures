############ Python based (ALL) ############
build_analysis_platfrom:
	./.build_graph.sh
pmcdoc_preprocessing:
	python tasks/preprocess_pmcdoc_pipeline.py
hp_preprocessing:
	python tasks/preprocess_hp_pipeline.py
	mkdir -p figures/graph; mv *.pdf figures/graph/

analyze_hp_graph:
	python tasks/process_hp_graph.py
	mkdir -p figures/graph; mv *.1.* figures/graph/
analyze_pmcdoc_ngram:
	python tasks/process_pmcdoc_ngram.py

extract_doc_word2vec:
	python tasks/extract_word2vec.py

extract_word2vec_distance:
	python tasks/extract_word2vec_distance.py

############ Debug (ALL) ############
calculate_graphs_similarity:
	python graph/pmcdoc_word2vec/cal_sim_graph.py

extract_doc_feature:
	python graph/pmcdoc_word2vec/extract_doc_feature.py

extract_phenotype_relationship:
	python graph/pmcdoc_word2vec/extract_relationship_phenotype.py
calculate_word2vec_distance:
	python graph/pmcdoc_word2vec/calculate_distance_of_word2vecs.py
