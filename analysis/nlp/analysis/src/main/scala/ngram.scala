import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.rdd.RDD
import scala.collection.mutable._


object NgramMain {
  import NgramUtilities._
  import StatUtilities._

	def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("Ngram")
                              .set("spark.broadcast.factory", "org.apache.spark.broadcast.TorrentBroadcastFactory")
                              .set("spark.io.compression.codec", "snappy")
                              .set("spark.broadcast.compress", "true")
                              .set("spark.akka.frameSize", "1024")
                              .set("spark.driver.maxResultSize", "16g")
                              .set("spark.shuffle.compress", "true")
                              .set("spark.rdd.compress", "true")
                              .set("spark.executor.cores", "4")

    val sc = new SparkContext(conf)
    val docPath: String = "data/all_in_one"
    val phenotypePath: String = "data/parsed_name"
    val numPartition: Int = 20
    val ifTakeSample: Boolean = true
    val sampleSize: Int = 1

    val phenoRDD: RDD[(String, Int)] = sc.textFile(phenotypePath, numPartition).mapPartitions({
      iter: Iterator[String] => for (line <- iter) yield splitPheno(line)
    }).filter(x => x._2 <= 4)
    val phenotypeBC: Broadcast[Array[(String, Int)]] = sc.broadcast(phenoRDD.collect())

    val originDocRDD: RDD[String] = sc.textFile(docPath, numPartition)
    val docRDD: RDD[String] =
      if (!ifTakeSample) originDocRDD
      else sc.parallelize( originDocRDD.take(sampleSize), numPartition )

    val ngramsDocRDD: RDD[(String, List[(String, Int)])] = docRDD.mapPartitions({
      iter: Iterator[String] => for (line <- iter) yield splitNgram(line, takeNgram, 1)
    }).cache()
    val numOfDoc: Long = ngramsDocRDD.count()

    val matchingTFCount: RDD[(String, (String, Int))] = ngramsDocRDD.flatMap(ngrams => phenotypeMatching(ngrams, phenotypeBC))
    val matchingPairs: RDD[(String, ListBuffer[(String, Int)])] = groupById(matchingTFCount)
    val matchingPairwise: RDD[((String, String), (Int, Int), String)] = matchingPairs.mapPartitions(buildPhenotypePairs)
    val matchingPairwiseScore: RDD[((String, String), Double, String)] = matchingPairwise.map(evaluatePhenptypesScore).cache()
    val matchingPairwiseTmp: RDD[((String, String), Int)] = groupByPair(matchingPairwiseScore)

    val cidf: RDD[((String, String), Double)] = matchingPairwiseTmp.map(c => (c._1, math.log((numOfDoc / c._2).toDouble)))
    val atf: RDD[((String, String), Double)] = calculateATF(matchingPairwiseScore)
    val statScore: RDD[((String, String), Double)] = calculateScore(cidf, atf, numOfDoc)

    sc.stop()
	}
}
