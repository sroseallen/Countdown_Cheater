import numpy as np
import random
from tqdm import tqdm
import time
import itertools
from threading import Thread


def generate_sums(numbers: list) -> dict:
    """
    Produces a dictionary of key:value pairs, where each key is a number possible to calculate from the entered list, and each value is the calculation to get there (see 'helper' function)

    Args
    numbers: list
    """
    results_dict = {}

    def helper(current_numbers, expression) -> tuple:
        """
        Function to find all possible numbers which can be created from the entered list using the following permitted operations:
        - Addition
        - Subtraction
        - Multiplication
        - Division (with only exact division permitted, integers only)

        Note: This function uses recursion and references itself in order to find every combination.
        """
        if len(current_numbers) == 1:
            if current_numbers[0] < 1:
                next
            else:
                results_dict[current_numbers[0]] = expression
            return

        # all combinations of pairs of numbers (i = first number, j = second number on iteration 1)
        for i in range(len(current_numbers)):
            for j in range(i + 1, len(current_numbers)):
                a, b = current_numbers[i], current_numbers[j]
                remaining = (
                    current_numbers[:i]
                    + current_numbers[i + 1 : j]
                    + current_numbers[j + 1 :]
                )

                # expression = empty string initially ("()")
                # Addition
                if expression:
                    helper([a + b] + remaining, f"{a} ({expression}) + {b}")
                else:
                    helper(
                        [a + b] + remaining, f"{a} + {b}"
                    )  # prevents empty strings being added to printed output if there is already an expression present for a and b

                # Subtraction
                if expression:
                    helper([a - b] + remaining, f"{a} ({expression}) - {b}")
                    helper([b - a] + remaining, f"{b} - {a} ({expression})")
                else:
                    helper([a - b] + remaining, f"{a} - {b}")
                    helper([b - a] + remaining, f"{b} - {a}")

                # Multiplication
                if expression:
                    helper([a * b] + remaining, f"{a} ({expression}) * {b}")
                else:
                    helper([a * b] + remaining, f"{a} * {b}")

                # Division
                if b != 0 and a % b == 0:
                    if expression:
                        helper([a // b] + remaining, f"{a} ({expression}) / {b}")
                    else:
                        helper([a // b] + remaining, f"{a} / {b}")
                if a != 0 and b % a == 0:
                    if expression:
                        helper([b // a] + remaining, f"{b} / {a} ({expression})")
                    else:
                        helper([b // a] + remaining, f"{b} / {a}")

    helper(numbers, "")
    return results_dict


def calculate_options(numbers: list) -> dict:
    """
    Runs through every possible combination of numbers from the entered list of 6, and for each combination, finds every value possible to calculate.
    """
    all_groups = []
    all_outputs = {}

    # Enters existing numbers into dictionary
    for i in numbers:
        all_outputs[i] = "In list"

    # Creates list of tuples of all combinations of the 6 numbers
    for num in range(2, len(numbers) + 1):
        new_group = list(itertools.combinations(numbers, num))
        all_groups.extend(new_group)

    # Creates all possible operations and resulting numbers for each tuple (each numerical combination)
    for group in all_groups:
        numbers = list(group)
        new_output = generate_sums(numbers)
        new_output.update(all_outputs)
        all_outputs = new_output

    # Returns dictionary of created numbers and the calculations which produced them
    return new_output


def countdown_timer():
    """
    Provides a little command line-printed timer to represent the 30-second clock in Countdown
    """
    print("TIME STARTS NOW!")
    for i in tqdm(range(30)):
        time.sleep(1)
    print("Enter answer.")


class ReturnThread(Thread):
    """
    Custom thread so I can get a return value from the calculate_options function
    Adapted from https://alexandra-zaharia.github.io/posts/how-to-return-a-result-from-a-python-thread/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return  # could alternatively raise an exception, depends on the use case
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f"{type(exc).__name__}: {exc}")

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result


# Mode 1: Play the game


# Set the numbers in play
def numbers_game():
    total_score = 0
    round_number = 1
    small_numbers = [
        i for i in range(1, 11) for _ in range(2)
    ]  # 1-10, each number appears twice
    large_numbers = [25, 50, 75, 100]

    # Contestant chooses numbers (0-4 large numbers), random selection of 6 tiles, target generated
    while round_number >= 1:
        print(f"ROUND {round_number}\n")
        chosen_large = int(input("How many large numbers would you like? (0-4)"))
        chosen_random = 6 - chosen_large

        numbers = []
        numbers.extend(random.sample(small_numbers, chosen_random))
        numbers.extend(random.sample(large_numbers, chosen_large))

        rng = np.random.default_rng()
        target = rng.integers(101, 999)

        # Start 30 second timer and calculate closest number in the background
        print(f"Your numbers are: {numbers}\n" + f"Your target is: {target}\n")

        t1 = ReturnThread(target=calculate_options, args=(numbers,))
        timer = Thread(target=countdown_timer)

        t1.start()
        timer.start()

        new_output = t1.join()
        closest_number = min(new_output, key=lambda x: abs(x - target))

        timer.join()
        answer = int(input("Enter answer now: "))

        # Scoring (10 points if exact, 7 if 1-5 away, 5 in 6-10 away, bonus 5 if matching the computer).
        score = 0
        if answer == target:
            score += 10
        elif abs(answer - target) <= 5:
            score += 7
        elif abs(answer - target) <= 10:
            score += 5
        else:
            score += 0

        print(f"Your answer was: {answer}")
        print(
            f"Computer found: {closest_number}\nCalculated by: {new_output.get(closest_number)}"
        )

        if answer == closest_number:
            score += 5
            print("Exact match with computer! 5 bonus points added.")

        total_score += score
        print(f"Your score for this round is: {score}")
        print(f"Your total score for this session is {total_score}. Play again?")

        play_again = input(f"Play again? Y / N")
        if play_again == "Y":
            round_number += 1
            next
            print(f"\n")
        elif play_again == "N":
            game_end = f"Final score: {total_score}. Thanks for playing!"
            return game_end


# Mode 2: Cheat the game
# Set the numbers in play


def numbers_cheat():
    numbers = []
    while len(numbers) < 6:
        new_num = int(input(f"Enter number {len(numbers) + 1}: "))
        numbers.append(new_num)
    print(numbers)

    # Set target number
    target = int(input("Enter target number: "))
    print(target)

    # Find closest answer to the target
    new_output = calculate_options(numbers)
    closest_number = min(new_output, key=lambda x: abs(x - target))
    answer = f"Computer found: {closest_number}, Calculated by: {new_output.get(closest_number)}"

    return answer
