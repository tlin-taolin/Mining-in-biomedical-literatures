import math._
import org.apache.spark.rdd.RDD
import scala.collection.mutable._
import org.apache.spark.broadcast.Broadcast

object StatUtilities {
  def groupByName(rdd: RDD[(String, (Int, Int))]): RDD[(String, ListBuffer[(Int, Int)])] = {
    val initialList = ListBuffer[(Int, Int)]()
    val addToList = (s: ListBuffer[(Int, Int)], v: (Int, Int)) => s += v
    val mergePartitionLists = (p1: ListBuffer[(Int, Int)], p2: ListBuffer[(Int, Int)]) => p1 ++ p2
    rdd.aggregateByKey(initialList)(addToList, mergePartitionLists)
  }

  def filterUseless(rdd: RDD[(String, ListBuffer[(Int, Int)])], matchingPattern: Int): RDD[(String, ListBuffer[(Int, Int)])] = {
    rdd.filter( x => x._2.exists( y => y._1 == matchingPattern) )
  }

  def flatDocLevel(matchings: Iterator[(String, ListBuffer[(Int, Int)])], phenoLabel: Int): Iterator[(Int, (String, Int))] = {
    /** perform a flatmap operation that can return
      * (docId, (pName, count))
      */
    for ( (matching, docIdsentIds) <- matchings;
          (docId, count) <- docIdsentIds.groupBy(w => w._1).mapValues(_.size).toList
          if ( docId != phenoLabel && count > 1)
        ) yield (docId, (matching, count))
  }

  def flatSentLevel(matchings: Iterator[(String, ListBuffer[(Int, Int)])], phenoLabel: Int): Iterator[(Int, (String, Int))] = {
    /** perform a flatmap operation that can return
      * (docId, (pName, count))
      */
    for ( (matching, docIdsentIds) <- matchings;
          (docIdsentId, count) <- docIdsentIds.groupBy(w => w).mapValues(_.size).toList
          if ( docIdsentId._1 != phenoLabel && count > 1)
        ) yield (docIdsentId._1, (matching, count))
  }

  def groupById(rdd: RDD[(Int, (String, Int))]): RDD[(Int, ListBuffer[(String, Int)])] = {
    val initialList = ListBuffer[(String, Int)]()
    val addToList = (s: ListBuffer[(String, Int)], v: (String, Int)) => s += v
    val mergePartitionLists = (p1: ListBuffer[(String, Int)], p2: ListBuffer[(String, Int)]) => p1 ++ p2
    rdd.aggregateByKey(initialList)(addToList, mergePartitionLists)
  }

  def buildPairs(docId: Int, pairs: ListBuffer[(String, Int)]): List[((String, String), (Int, Int), Int)] = {
    pairs.flatMap( pair1 =>
      pairs.map(pair2 => ((pair1._1, pair2._1), (pair1._2, pair2._2), docId) ) ).toList
  }

  def evaluatePhenptypesScore(inTuples: Iterator[((String, String), (Int, Int), Int)], weight: Double): Iterator[((String, String), Double, Int)] = {
    def addWeight(m: Double): Double = min(m, weight) / weight
    for (inTuple <- inTuples;
      minTuple: Double = min(inTuple._2._1, inTuple._2._2).toDouble;
      maxTuple: Double = max(inTuple._2._1, inTuple._2._2).toDouble;
      score: Double =  minTuple / log(1 + maxTuple) * addWeight(minTuple)
    ) yield (inTuple._1, score, inTuple._3)
  }

  def groupByPair(rdd: RDD[((String, String), Double, Int)]): RDD[((String, String), (Double, Int))] = {
    val addToCounts = (s: (Double, Int), v: Double) => (s._1 + v, s._2 + 1)
    val sumPartition = (s1: (Double, Int), s2: (Double, Int)) => (s1._1 + s2._1, s1._2 + s2._2)
    rdd.map(x => (x._1, x._2)).aggregateByKey((0.0, 0))(addToCounts, sumPartition)
  }

  def calculateATF(rdd: RDD[((String, String), Double, Int)]): RDD[((String, String), Double)] = {
    val addToSum = (s: Double, v: Double) => s + v
    val sumPartition = (s1: Double, s2: Double) => s1 + s2
    rdd.map(x => (x._1, x._2)).aggregateByKey(0.0)(addToSum, sumPartition)
  }

  def calculateScore(rddCIDF: RDD[((String, String), Double)], rddATF: RDD[((String, String), Double)], numOfDoc: Long): RDD[((String, String), Double)] = {
    rddCIDF.cogroup(rddATF).map{ x => ( x._1, x._2._1.reduce(_ * _) * x._2._2.reduce(_ * _) / numOfDoc)}
  }
}
