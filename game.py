import random
from logic import feedback


class Mastermind:
    DIFFICULTIES = {
        "1": {"name": "Easy", "length": 3, "symbols": "1234", "turns": 12},
        "2": {"name": "Medium", "length": 4, "symbols": "123456", "turns": 10},
        "3": {"name": "Hard", "length": 5, "symbols": "12345678", "turns": 8},
    }

    def __init__(self, difficulty=None):
        self.history = []
        self.ended = False
        self.difficulty = None
        self.code = []
        self.turns = 0

        if difficulty in self.DIFFICULTIES:
            self._set_difficulty(difficulty)

    def _set_difficulty(self, difficulty):
        settings = self.DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.code = [
            random.choice(settings["symbols"]) for _ in range(settings["length"])
        ]
        self.history = []
        self.turns = settings["turns"]
        self.ended = False

    def _choose_difficulty(self):
        print("Choose difficulty:")
        for key, settings in self.DIFFICULTIES.items():
            print(
                f"{key}. {settings['name']} "
                f"({settings['length']} digits, "
                f"symbols 1-{settings['symbols'][-1]}, "
                f"{settings['turns']} turns)"
            )

        while True:
            choice = input("Difficulty > ").strip()
            if choice in self.DIFFICULTIES:
                return choice
            print("Enter 1, 2, or 3.")

    def _show_history(self):
        if not self.history:
            print("No guesses yet.")
            return

        print("\nGuess history:")
        for number, (guess, exact, partial) in enumerate(self.history, 1):
            print(
                f"{number:>2}. {guess}  "
                f"Exact: {exact}  Partial: {partial}"
            )

    def _valid_guess(self, raw):
        settings = self.DIFFICULTIES[self.difficulty]
        return (
            len(raw) == settings["length"]
            and all(ch in settings["symbols"] for ch in raw)
        )

    def run(self):
        # Once the game ends, calling run() again cannot change its state.
        if self.ended:
            return

        if self.difficulty is None:
            self._set_difficulty(self._choose_difficulty())

        settings = self.DIFFICULTIES[self.difficulty]
        print(
            f"\nMastermind — {settings['name']}: "
            f"enter {settings['length']} digits using "
            f"1-{settings['symbols'][-1]}."
        )
        print("Enter 'h' to view history or 'q' to quit.")

        while self.turns > 0 and not self.ended:
            raw = input(f"{self.turns} turns left > ").strip().lower()

            if raw == "q":
                self.ended = True
                print("Game quit.")
                return

            if raw == "h":
                self._show_history()
                continue

            if not self._valid_guess(raw):
                print(
                    f"Enter exactly {settings['length']} digits "
                    f"using only 1-{settings['symbols'][-1]}."
                )
                continue

            exact, partial = feedback(self.code, list(raw))
            self.history.append((raw, exact, partial))
            self.turns -= 1

            print("Exact:", exact, " Partial:", partial)

            if exact == len(self.code):
                self.ended = True
                print("Cracked the code!")
                self._show_history()
                return

        if not self.ended:
            self.ended = True
            print("Out of turns.")
            print("The code was", "".join(self.code))
            self._show_history()
