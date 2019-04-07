object Calculators {

  type GuessCalculator = (Set[Char], Int, Stream[String], Stream[String]) => Stream[(String, Long)]

  val BFM: GuessCalculator = (alphabet, minimumPasswordLength, trainingSet, passwordsToGuess) => {
    def calculateFirstCharRanks: Map[Char, Int] = {
      val firstCharFrequency: Map[Char, Int] = trainingSet
        .groupBy(_.charAt(0)) //Map(firstChar, List(password)
        .map { case (firstCharacter, passwords) => (firstCharacter, passwords.size) }

      val missingChars = alphabet.diff(firstCharFrequency.keySet)

      (firstCharFrequency ++ missingChars.map((_, 0))).toVector
        .sortBy(-_._2)
        .map(_._1)
        .zipWithIndex
        .toMap
    }

    def calculateDigramRanks: Map[String, Int] = {
      val digrams: Stream[String] = trainingSet.flatMap(_.sliding(2, 1))

      val missingFirstChars = alphabet.diff(digrams.map(_.charAt(0)).toSet)

      (digrams.groupBy(_.charAt(0)) ++ missingFirstChars.map((_, Stream.empty[String])))
        .flatMap { case (firstChar, digrams) =>
          val secondCharFrequency: Map[Char, Int] = digrams
            .groupBy(_.charAt(1))
            .map { case (secondChar, digrams) => (secondChar, digrams.size) }

          val missingChars = alphabet.diff(secondCharFrequency.keySet)

          (secondCharFrequency ++ missingChars.map((_, 0)))
            .toVector
            .sortBy(-_._2)
            .map { case (secondChar, _) => s"$firstChar$secondChar" }
            .zipWithIndex
        }
    }

    val firstCharacterRanks = calculateFirstCharRanks
    val digramRanks = calculateDigramRanks

    println(firstCharacterRanks)
    println(digramRanks)

    def calculateGuesses(password: String): Long = {
      val shorterGuesses = (minimumPasswordLength until password.length) // guesses that are shorter than the password and longer than minimum password length
        .map(math.pow(alphabet.size, _))
        .sum

      val wrongFirstCharGuesses = firstCharacterRanks(password.charAt(0)) * math.pow(alphabet.size, password.length - 1) // guesses with wrong first character

      val wrongNthCharGuesses = password.sliding(2, 1)
        .zipWithIndex
        .map { case (digram, index) => digramRanks(digram) * math.pow(alphabet.size, password.length - (index + 2)) }
        .sum

      (shorterGuesses + wrongFirstCharGuesses + wrongNthCharGuesses).toLong
    }

    passwordsToGuess.map(password => (password, calculateGuesses(password)))
  }
}
