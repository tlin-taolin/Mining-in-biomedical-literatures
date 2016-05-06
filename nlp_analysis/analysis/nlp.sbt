name := "NLP Analysis"

version := "1.0"

scalaVersion := "2.10.5"

libraryDependencies ++= Seq(
"org.apache.spark" %% "spark-core" % "1.6.0",
"org.apache.spark" %% "spark-mllib" % "1.6.0"
)

resolvers += "Akka Repository" at "http://repo.akka.io/releases/"
