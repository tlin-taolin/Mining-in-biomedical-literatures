import math._
import org.apache.spark.rdd.RDD
import scala.collection.mutable._
import org.apache.spark.broadcast.Broadcast

object StatUtilities {

  def stringDistance1(s1: String, s2: String): Int = {
    val memo = scala.collection.mutable.Map[(List[Char], List[Char]), Int]()
    def minimum(a: Int, b: Int, c: Int) = min(min(a, b), c)
    def sd(s1: List[Char], s2: List[Char]): Int = {
      if (memo.contains((s1, s2)) == false)
        memo((s1,s2)) = (s1, s2) match {
          case (_, Nil) => s1.length
          case (Nil, _) => s2.length
          case (c1::t1, c2::t2)  => minimum(sd(t1, s2) + 1,
                                            sd(s1, t2) + 1,
                                            sd(t1, t2) + (if (c1 == c2) 0 else 1))
      }
      memo((s1,s2))
    }
    sd( s1.toList, s2.toList )
  }

  def stringDistance2(s1: String, s2: String): Int = {
    if (s1.split(" ").toList.equals(s2.split(" ").toList)) 0
    else 10
  }

  def findTFInDoc(pheno: (String, Int), ngram: (String, Int), threshold: Int): Int = {
    if (pheno._2 == ngram._2) {
      val dist = stringDistance1(pheno._1, ngram._1)
      if (dist <= threshold) 1
      else 0
    }
    else 0
  }

  def phenotypeMatching(ngrams: (String, List[(String, Int)]),
                        phenoBD: Broadcast[Array[(String, Int)]]
                       ): List[(String, (String, Int))] = {
    val (id, nngram) = ngrams
    nngram.flatMap(ngram => phenoBD.value.map(
      pheno => ( id, (pheno._1, findTFInDoc(pheno, ngram, 3)) )
    )).filter( line => line._2._2 != 0)
  }

  def groupById(rdd: RDD[(String, (String, Int))]): RDD[(String, ListBuffer[(String, Int)])] = {
    val initialList = ListBuffer[(String, Int)]()
    val addToList = (s: ListBuffer[(String, Int)], v: (String, Int)) => s += v
    val mergePartitionLists = (p1: ListBuffer[(String, Int)], p2: ListBuffer[(String, Int)]) => p1 ++ p2
    rdd.aggregateByKey(initialList)(addToList, mergePartitionLists)
  }

  def buildPhenotypePairs(iterPairs: Iterator[(String, ListBuffer[(String, Int)])]): Iterator[((String, String), (Int, Int), String)] = {
    for ((docId, pairs) <- iterPairs;
          pair1 <- pairs;
          pair2 <- pairs;
          // pairsWithIndex = pairs.zipWithIndex;
          // (pair1, ind1) <- pairsWithIndex;
          // (pair2, ind2) <- pairsWithIndex;
          // if (ind1 < ind2)
          if (pair1 != pair2)
    ) yield ((pair1._1, pair2._1), (pair1._2, pair2._2), docId)
  }

  def evaluatePhenptypesScore(inTuple: ((String, String), (Int, Int), String)): ((String, String), Double, String) = {
    val score: Double = 1.0 - 2.0 * min(inTuple._2._1, inTuple._2._2) / (inTuple._2._1 + inTuple._2._2)
    (inTuple._1, score, inTuple._3)
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
