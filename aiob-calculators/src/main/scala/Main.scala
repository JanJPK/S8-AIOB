import java.io.File
import java.nio.file.Files
import java.util.stream.{Stream => JStream}
import java.util.{Iterator => JIterator}

object Main extends App {
  def convertJavaStreamToScalaStream[A](stream: JStream[A]): Stream[A] = {
    val it = stream.iterator()

    def fromIterator(it: JIterator[A]): Stream[A] =
      if (it.hasNext) Stream.cons(it.next(), fromIterator(it)) else { stream.close(); Stream.empty }

    fromIterator(it)
  }

  def readPasswordsFromFile(file: File): Stream[String] = {
    convertJavaStreamToScalaStream(Files.lines(file.toPath))
  }

  val Alphabet1 = (('a' to 'z') ++ ('0' to '9')).toSet
  val Alphabet2 = (('a' to 'z') ++ ('0' to '9') ++ ('A' to 'Z')).toSet

  val result1 = Calculators.BFM(
    Alphabet1,
    5,
    readPasswordsFromFile(new File("trainingSet.txt")),
    Stream("princes"))

  val result2 = Calculators.BFM(
    Alphabet2,
    5,
    readPasswordsFromFile(new File("trainingSet3.txt")),
    readPasswordsFromFile(new File("trainingSet.txt")))

  println(result2.mkString("\n"))
}
