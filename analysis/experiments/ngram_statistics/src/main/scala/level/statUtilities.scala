import math._
import org.apache.spark.rdd.RDD
import scala.collection.mutable._
import org.apache.spark.broadcast.Broadcast

object StatUtilities {
  def groupByName(rdd: RDD[(String, (String, Int))]): RDD[(String, ListBuffer[(String, Int)])] = {
    val initialList = ListBuffer[(String, Int)]()
    val addToList = (s: ListBuffer[(String, Int)], v: (String, Int)) => s += v
    val mergePartitionLists = (p1: ListBuffer[(String, Int)], p2: ListBuffer[(String, Int)]) => p1 ++ p2
    rdd.aggregateByKey(initialList)(addToList, mergePartitionLists)
  }

  def filterUseless(rdd: RDD[(String, ListBuffer[(String, Int)])], matchingPattern: String): RDD[(String, ListBuffer[(String, Int)])] = {
    rdd.filter( x => x._2.exists( y => y._1 == matchingPattern) )
  }

  def flatSentLevel(matchings: Iterator[(String, ListBuffer[(String, Int)])], phenoLabel: String): Iterator[(String, (String, Int))] = {
    /** perform a flatmap operation that can return
      * (docId, (pName, count))
      */
    for ( (matching, docIdsentIds) <- matchings;
          (docIdsentId, count) <- docIdsentIds.groupBy(w => w).mapValues(_.size).toList
          if ( docIdsentId._1 != phenoLabel)
        ) yield (docIdsentId._1, (matching, count))
  }

  def flatDocLevel(matchings: Iterator[(String, ListBuffer[(String, Int)])], phenoLabel: String): Iterator[(String, (String, Int))] = {
    /** perform a flatmap operation that can return
      * (docId, (pName, count))
      */
    for ( (matching, docIdsentIds) <- matchings;
          (docIdsentId, count) <- docIdsentIds.groupBy(w => w._1).mapValues(_.size).toList
          if ( docIdsentId != phenoLabel)
        ) yield (docIdsentId, (matching, count))
  }

  def groupById(rdd: RDD[(String, (String, Int))]): RDD[(String, ListBuffer[(String, Int)])] = {
    val initialList = ListBuffer[(String, Int)]()
    val addToList = (s: ListBuffer[(String, Int)], v: (String, Int)) => s += v
    val mergePartitionLists = (p1: ListBuffer[(String, Int)], p2: ListBuffer[(String, Int)]) => p1 ++ p2
    rdd.aggregateByKey(initialList)(addToList, mergePartitionLists)
  }

  def buildPairs(docId: String, pairs: ListBuffer[(String, Int)]): List[((String, String), (Int, Int), String)] = {
    pairs.flatMap( pair1 =>
      pairs.map(pair2 => ((pair1._1, pair2._1), (pair1._2, pair2._2), docId) ) ).toList
  }

  def evaluatePhenptypesScore(inTuples: Iterator[((String, String), (Int, Int), String)]): Iterator[((String, String), Double, String)] = {
    for (inTuple <- inTuples;
      score: Double = 1.0 - 2.0 * min(inTuple._2._1, inTuple._2._2) / (inTuple._2._1 + inTuple._2._2)
    ) yield (inTuple._1, score, inTuple._3)
  }

  def groupByPair(rdd: RDD[((String, String), Double, String)]): RDD[((String, String), Int)] = {
    val addToCounts = (s: Int, v: Double) => s + 1
    val sumPartition = (s1: Int, s2: Int) => s1 + s2
    rdd.map(x => (x._1, x._2)).aggregateByKey(0)(addToCounts, sumPartition)
  }

  def calculateATF(rdd: RDD[((String, String), Double, String)]): RDD[((String, String), Double)] = {
    val addToSum = (s: Double, v: Double) => s + v
    val sumPartition = (s1: Double, s2: Double) => s1 + s2
    rdd.map(x => (x._1, x._2)).aggregateByKey(0.0)(addToSum, sumPartition)
  }

  def calculateScore(rddCIDF: RDD[((String, String), Double)], rddATF: RDD[((String, String), Double)], numOfDoc: Long): RDD[((String, String), Double)] = {
    rddCIDF.cogroup(rddATF).map{ x => ( x._1, x._2._1.reduce(_ * _) * x._2._2.reduce(_ * _) / numOfDoc)}
  }
}
