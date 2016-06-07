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

  def flatSentLevel(matchings: Iterator[(String, ListBuffer[(Int, Int)])],
                    phenoLabel: Int): Iterator[(Int, Int)] = {
    /** perform a flatmap operation that can return
      * (docId, (pName, count))
      */
    for ( (matching, docIdsentIds) <- matchings;
          (docIdsentId, count) <- docIdsentIds
                                    .groupBy(w => w)
                                    .mapValues(_.size)
                                    .toList
          if ( docIdsentId._1 != phenoLabel && count > 1)
        ) yield docIdsentId
  }

  def extractSent(matchingIds: List[Int],
                  cops: List[(String, Int)]): List[String] = {
    /** Extract the valid sentence from the documents,
      * based on given matching id list, and dictionary list.
      */
    Set(matchingIds: _*).toList.flatMap(x => cops.filter(y => x == y._2).map(y => y._1))
  }
}
