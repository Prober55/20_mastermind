def feedback(code, guess):
    """Return (exact, partial) matches without reusing code occurrences."""
    exact = 0
    remaining_code = []
    remaining_guess = []

    # Exact matches are resolved first.
    for code_symbol, guess_symbol in zip(code, guess):
        if code_symbol == guess_symbol:
            exact += 1
        else:
            remaining_code.append(code_symbol)
            remaining_guess.append(guess_symbol)

    # Each remaining code occurrence can be used only once.
    partial = 0
    for guess_symbol in remaining_guess:
        if guess_symbol in remaining_code:
            partial += 1
            remaining_code.remove(guess_symbol)

    return exact, partial
