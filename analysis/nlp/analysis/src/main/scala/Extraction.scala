import java.io.File
import scala.io.Source
import scala.util.parsing.json._
import scala.util.matching.Regex

case class MapTuple(value: Map[String, List[String]])

//import org.apache.spark.SparkContext
//import org.apache.spark.SparkContext._
//import org.apache.spark.SparkConf
//import org.apache.spark.mllib.linalg.Vectors
//import org.apache.spark.rdd.RDD


object utilities {
	def loadJson(path: String): List[String] = {
		val parsedFiles: List[File] = new File(path).listFiles.filter(_.isFile).toList
		val docs: List[String] = parsedFiles.map(parseJson(_))
		docs
	}

	def parseJson(file: File): String = {
		println("Processing :" + file.toString())
		val t: Iterator[String] = Source.fromFile(file).getLines()
		JSON.parseFull(t.toList(0)) match {
			case Some(MapTuple(m)) => m("abstract").reduce((a, b) => a + b)
			case _ => ""
		}
	}

	def loadText(path: String): List[String] = {
		val docs: List[String] = Source.fromFile(path).getLines
									   .mkString("\n").split("\n").toList
		val docsList: List[List[String]] = docs.map(_.split("""\s+""").toList)
		println(docs)
		println(docsList)
		docs
	}

}

object Extraction {
	def main(args: Array[String]): Unit = {
		val dataDir: String = "../data/parsed"
		val dataPath: String = "../data/test.txt"
		// val linesJson: List[String] = utilities.loadJson(dataDir)
		val linesText: List[String] = utilities.loadText(dataPath)
	}
}
