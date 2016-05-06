import java.io.File
import scala.io.Source
import scala.util.parsing.json._

case class MapTuple(value: Map[String, List[String]])

//import org.apache.spark.SparkContext
//import org.apache.spark.SparkContext._
//import org.apache.spark.SparkConf
//import org.apache.spark.mllib.linalg.Vectors
//import org.apache.spark.rdd.RDD


object utilities {
	def loadsJson(path: String): List[File] = {
		val parsedFiles: List[File] = new File(path).listFiles.filter(_.isFile).toList
		val docs: List[String] = parsedFiles.map(parse(_))

		parsedFiles
	}

	def parse(file: File): String = {
		println("Processing :" + file.toString())
		val t: Iterator[String] = Source.fromFile(file).getLines()
		JSON.parseFull(t.toList(0)) match {
			case Some(MapTuple(m)) => m("abstract").reduce((a, b) => a + b)
			case _ => ""
		}
	}

}

object Extraction {
	def main(args: Array[String]): Unit = {
		val dataPath: String = "../data/parsed"
		val lines: List[File] = utilities.loadsJson(dataPath)
	}
}
