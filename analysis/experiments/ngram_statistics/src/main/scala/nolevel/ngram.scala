import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.rdd.RDD
import scala.collection.mutable._


object NgramNoLevel {
  import NgramUtilitiesNoLevel._
  import StatUtilitiesNoLevel._

  def setPara(): Map[String, Any] = {
    Map("sizeNgram" -> List(1),
        "numPartition" -> 300,
        "ifTakeSample" -> true,
        "sampelSize" -> 10
       )
  }

	def main(args: Array[String]): Unit = {
    /* Configure Spark */
    val conf = new SparkConf().setAppName("Ngram")
                              .set("spark.broadcast.factory", "org.apache.spark.broadcast.TorrentBroadcastFactory")
                              .set("spark.io.compression.codec", "snappy")
                              .set("spark.broadcast.compress", "true")
                              .set("spark.akka.frameSize", "1024")
                              .set("spark.driver.maxResultSize", "8g")
                              .set("spark.shuffle.compress", "true")
                              .set("spark.rdd.compress", "true")

    val sc = new SparkContext(conf)

    /* Configure parameters */
    val docPath: String = "data/all_in_one"
    val phenotypePath: String = "data/parsed_name"
    val parameters: Map[String, Any] = setPara()
    val sizeNgram: List[Int] = parameters("sizeNgram").asInstanceOf[List[Int]]
    val numPartition: Int = parameters("numPartition").asInstanceOf[Int]
    val ifTakeSample: Boolean = parameters("ifTakeSample").asInstanceOf[Boolean]
    val sampleSize: Int = parameters("sampelSize").asInstanceOf[Int]

    /* read data to RDD */
    val originDocRDD: RDD[String] = sc.textFile(docPath, numPartition)
    val docRDD: RDD[String] =
      if (!ifTakeSample) originDocRDD
      else sc.parallelize( originDocRDD.take(sampleSize), numPartition )
    val phenoRDD: RDD[String] = sc.textFile(phenotypePath, numPartition).mapPartitions({
      iter: Iterator[String] => for (line <- iter) yield splitPheno(line)
    }).filter(x => x._2 <= 4).map(_._1)

    /* processing the data and save to file */
    for (sizeN <- sizeNgram;
      statScore = processing(originDocRDD, phenoRDD, sizeN)
    ) yield statScore.saveAsTextFile("statScore-" + sizeN)

    sc.stop()
	}

  def processing(docRDD: RDD[String], phenoRDD: RDD[String], sizeN: Int): RDD[((String, String), Double)] = {
    /* set parameters */
    val phenoLabel: String = "phenotype"

    /* split ngram */
    val ngramsDocRDD: RDD[(String, List[String])] = docRDD.mapPartitions({
      iter: Iterator[String] => for (line <- iter) yield splitNgram(line, takeNgram, sizeN)
    }).cache()
    val numOfDoc: Long = ngramsDocRDD.count()

    println("test1")

    /* get valid ngram information (join phenotype dictionary with doc ngrams) */
    val reverseNgramRDD: RDD[(String, String)] = ngramsDocRDD.mapPartitions({
      iterator: Iterator[(String, List[String])] => for ((id, lines) <- iterator; line <- lines) yield (line, id)
    })
    val reversePhenoRDD: RDD[(String, String)] = phenoRDD.map(x => (x, phenoLabel))
    val reverseRDD: RDD[(String, String)] = reverseNgramRDD.union(reversePhenoRDD).cache()
    val groupedRDD: RDD[(String, ListBuffer[String])] = groupByName(reverseRDD).cache()
    val matchingRDD: RDD[(String, ListBuffer[String])] = filterUseless(groupedRDD, phenoLabel).cache()

    /* calculation for ngram statistics, i.e., tf, atf. cidf */
    val idTFCountRDD: RDD[(String, (String, Int))] = matchingRDD.mapPartitions({
      iterator: Iterator[(String, ListBuffer[String])] =>
        for ((matchingName, docIds) <- iterator;
            (docId, count) <- docIds.groupBy(w => w).mapValues(_.size).toList
            if (docId != phenoLabel)
          ) yield (docId, (matchingName, count))
    }).cache()

    val groupedIdTFCountRDD: RDD[(String, ListBuffer[(String, Int)])] = groupById(idTFCountRDD).cache()
    val pairwiseWithGroupedId: RDD[((String, String), (Int, Int), String)] = groupedIdTFCountRDD.flatMap(x => buildPairs(x._1, x._2)).cache()
    val pairwiseScoreWithGroupedId: RDD[((String, String), Double, String)] = pairwiseWithGroupedId.mapPartitions(evaluatePhenptypesScore).cache()
    val matchingPairwiseTmp: RDD[((String, String), Int)] = groupByPair(pairwiseScoreWithGroupedId).cache()
    val cidf: RDD[((String, String), Double)] = matchingPairwiseTmp.map(c => (c._1, math.log((1.0 * numOfDoc / c._2).toDouble)))
    val atf: RDD[((String, String), Double)] = calculateATF(pairwiseScoreWithGroupedId)
    val statScore: RDD[((String, String), Double)] = calculateScore(cidf, atf, numOfDoc)
    statScore
  }

}
