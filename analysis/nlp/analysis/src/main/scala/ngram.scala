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
    val sc = new SparkContext(conf)
    val docPath: String = "../data/test"
    val phenotypePath: String = "../data/graph/parsed_name"
    val numPartition: Int = 8

    val phenoRDD: RDD[(String, Int)] = sc.textFile(phenotypePath).map(line => splitPheno(line))
    val phenotypeBC: Broadcast[Array[(String, Int)]] = sc.broadcast(phenoRDD.collect())

    val originDocRDD: RDD[String] = sc.textFile(docPath, numPartition)
    val ngramsDocRDD: RDD[(String, List[(String, Int)])] = originDocRDD.map(line => splitNgram(line, takeNgrams, 4)).cache()
    val numOfDoc: Long = ngramsDocRDD.count()

    val matchingTFCount: RDD[(String, (String, Int))] = ngramsDocRDD.flatMap(ngrams => phenotypeMatching(ngrams, phenotypeBC))
    val matchingPairs: RDD[(String, ListBuffer[(String, Int)])] = groupById(matchingTFCount)
    val matchingPairwise: RDD[((String, String), (Int, Int), String)] = matchingPairs.mapPartitions(buildPhenotypePairs)
    val matchingPairwiseScore: RDD[((String, String), Float, String)] = matchingPairwise.map(evaluatePhenptypesScore)
    val matchingPairwiseTmp: RDD[((String, String), Int)] = groupByPair(matchingPairwiseScore)
    val matchingCIDF: RDD[((String, String), Double)] = matchingPairwiseTmp.map(c => (c._1, math.log((numOfDoc / c._2).toDouble)))

    sc.stop()
	}
}
