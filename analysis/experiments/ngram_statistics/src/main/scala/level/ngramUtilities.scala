import org.apache.spark.rdd.RDD

object NgramUtilities {
  def splitLines(lines: String): (Int, List[(String, Int)]) = {
    val splitedLine: Array[String] = lines.split("::")
    if (splitedLine.length == 2)
      (splitedLine(0).toInt, splitedLine(1).split("""\.\.\.""").toList.zipWithIndex)
    else
      (splitedLine(0).toInt, List())
  }

  def updateLastElement(l: List[String]): List[String] = {
    /** Deal with the corner case, e.g., remove the `.` and blank */
    val tmp: String = l(l.size - 1)
    l.updated(l.size - 1, tmp.dropRight(1).trim)
  }

  def takeNgram(sentence: (String, Int), n: Int): List[(String, Int)] = {
    /** Take ngram for each sentence. */
    def helper(words: List[String]): List[List[String]] = {
      words match {
        case h::t if (words.length >= n) => words.take(n) :: helper(t)
        case _ => Nil
      }
    }
    val splited_sentence: List[String] = sentence._1.trim.split(" ").toList
    helper(updateLastElement(splited_sentence)).map(x => (x.mkString(" "), sentence._2))
  }

  def takeNgrams(sent: (String, Int), n: Int): List[(String, Int)] = {
    /** Take each `nn`-gram for each sentence. Here, 1 <= `nn` <= n. */
    (1 until (n + 1)).flatMap(ind => takeNgram(sent, ind)).toList
  }

  def splitNgram(lines: String, takeN: ((String, Int), Int) => List[(String, Int)], n: Int): (Int, List[(String, Int)]) = {
    /** Split the input sentence to the following format.
      * (docId, List[(ngram, sentId)])
      */
    val (docId, alines): (Int, List[(String, Int)]) = splitLines(lines)
    val ngrams: List[(String, Int)] = alines.flatMap(sentence => takeN(sentence, n))
    (docId, ngrams)
  }

  def splitPheno(lines: String): (String, Int) = {
    (lines, lines.split(" ").length)
  }

  def revertNgram(iterator: Iterator[(Int, List[(String, Int)])]): Iterator[(String, (Int, Int))] = {
      for ((docId, ngrams) <- iterator; (ngram, sentId) <- ngrams)
        yield (ngram, (docId, sentId))
  }
}
