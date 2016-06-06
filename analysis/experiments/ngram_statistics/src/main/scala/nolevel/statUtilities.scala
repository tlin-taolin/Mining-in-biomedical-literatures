import math._
import org.apache.spark.rdd.RDD
import scala.collection.mutable._
import org.apache.spark.broadcast.Broadcast

object StatUtilitiesNoLevel {
  def groupByName(rdd: RDD[(String, String)]): RDD[(String, ListBuffer[String])] = {
    val initialList = ListBuffer[String]()
    val addToList = (s: ListBuffer[String], v: String) => s += v
    val mergePartitionLists = (p1: ListBuffer[String], p2: ListBuffer[String]) => p1 ++ p2
    rdd.aggregateByKey(initialList)(addToList, mergePartitionLists)
  }

  def filterUseless(rdd: RDD[(String, ListBuffer[String])], matchingPattern: String): RDD[(String, ListBuffer[String])] = {
    rdd.filter(x => x._2.exists( y => y == matchingPattern))
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
