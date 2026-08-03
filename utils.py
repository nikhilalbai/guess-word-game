def check_guess(secret_word, guess_word):

    colors = []

    for i in range(5):

        if guess_word[i] == secret_word[i]:
            colors.append("green")

        elif guess_word[i] in secret_word:
            colors.append("orange")

        else:
            colors.append("gray")

    return colors