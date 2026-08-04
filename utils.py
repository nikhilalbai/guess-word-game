def check_guess(secret_word, guess_word):

    secret_word = secret_word.upper()
    guess_word = guess_word.upper()

    colors = ["gray"] * 5

    # Convert secret word into a list
    remaining_letters = list(secret_word)

    # --------------------------
    # Pass 1 - Check Green
    # --------------------------

    for i in range(5):

        if guess_word[i] == secret_word[i]:

            colors[i] = "green"

            remaining_letters[i] = None

    # --------------------------
    # Pass 2 - Check Orange
    # --------------------------

    for i in range(5):

        if colors[i] == "green":
            continue

        if guess_word[i] in remaining_letters:

            colors[i] = "orange"

            index = remaining_letters.index(guess_word[i])

            remaining_letters[index] = None

    return colors