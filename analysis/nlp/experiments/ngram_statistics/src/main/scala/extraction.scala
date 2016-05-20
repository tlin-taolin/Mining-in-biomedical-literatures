import java.io.File
import scala.io.Source
import scala.util.parsing.json._
import scala.util.matching.Regex

case class MapTuple(value: Map[String, List[String]])

object Utilities {
	def load(path: String, loadFile: File => String): List[String] = {
		val parsedFiles: List[File] = new File(path).listFiles.filter(_.isFile).toList
		val docs: List[String] = parsedFiles.map(loadFile(_))
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
		docs
	}

}

object Extraction {
	def main(args: Array[String]): Unit = {
		val dataDir: String = "../data/parsed/"
		val dataPath: String = "../data/test.txt"
		val linesJson: List[String] = Utilities.load(dataDir, Utilities.parseJson)
		// val linesText: List[String] = utilities.loadText(dataPath)
	}
}
