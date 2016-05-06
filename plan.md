[x] Use scripts to deploy a computation cluster on the top of Google cloud.

---

[] Download some public datasets, and apply my approaches on these datasets.

* It can be either a baseline algorithm or as an auxiliary for my approach.
* It can be used as an evaluation.

---

[] Apply traditional approach to extract the relationship on my dataset, and tried to use statistical approach to quantify the relationship.

* e.g., co-occurrence

---

## how to use trained word2vec result.
1. obtain word2vec
2. combine/merge the word2vec of the phenotype
3. inspired by the intrinsic evaluation, try to get the relationship word2vec of each two phenotype word2vec. And output it to the dataset.
4. discover the pattern among the dataset produced by step 3. e.g., unsupervised clustering, find the most frequent relationship pattern.

some basic idea:

* map these relationship word2vec to the graph, i.e., quantify the phenotype relationship.
* obtain sentence2vec, and calculate the distance of each sentence2vec with each phenotype word2vec.
    * find out the sentence that may contain the meaning of the phenotype.
    * based on these sentences that contains the phenotype, we can further our process of relationship extraction.
* apply CNN to word2vec, and do the relationship extraction.
* combine/merge the word2vec of any n-gram for each sentence. for these word2vec, we can calculate its distance with all phenotype word2vec. and for each phenotype, find out its top-k ngram phase.
