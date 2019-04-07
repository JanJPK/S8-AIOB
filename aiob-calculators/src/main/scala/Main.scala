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

  val Alphabet = Set('a', 'b', 'c')

  val result = Calculators.BFM(Alphabet, 2, Stream("aaa", "aba"), Stream("abac"))
  println(result.mkString("\n"))
}
