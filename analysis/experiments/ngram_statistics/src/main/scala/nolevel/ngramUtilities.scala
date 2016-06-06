import org.apache.spark.rdd.RDD


object NgramUtilitiesNoLevel {
  def splitLines(lines: String): (String, List[String]) = {
    val splitedLine: Array[String] = lines.split("::")
    if (splitedLine.length == 2)
      (splitedLine(0), splitedLine(1).split("""\.\.\.""").toList)
    else
      (splitedLine(0), List())
  }

  def takeNgram(words: List[String], n: Int): List[String] = {
    /* Take ngram for each sentence. */
    def helper(words: List[String]): List[List[String]] = {
      words match {
        case h::t if (words.length >= n) => words.take(n) :: helper(t)
        case _ => Nil
      }
    }
    helper(words).map(x => x.mkString(" "))
  }

  def takeNgrams(sent: List[String], n: Int): List[String] = {
    /* Take each `nn`-gram for each sentence. Here, 1 <= `nn` <= n. */
    (1 until n).flatMap(ind => takeNgram(sent, ind)).toList
  }

  def splitNgram(lines: String, takeN: (List[String], Int) => List[String], n: Int): (String, List[String]) = {
    val (id, alines): (String, List[String]) = splitLines(lines)
    val ngram: List[String] = alines.flatMap(s => takeN(s.split(" ").toList, n))
    (id, ngram)
  }

  def splitPheno(lines: String): (String, Int) = {
    (lines, lines.split(" ").length)
  }

}
