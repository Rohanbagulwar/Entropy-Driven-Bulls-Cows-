"""Bulls and Cows (Entropy Edition)

This module implements a command-line Bulls and Cows game with an
entropy-based AI hint system. The AI recommends guesses by computing
expected information gain (Shannon entropy) over the candidate pool.

Usage:
    python main.py

"""

import random
import math
import itertools
from collections import Counter
import time

# ------------------------------------------------------------------------------
# Video Links 
# ------------------------------------------------------------------------------
# Demonstration Video: https://www.youtube.com/watch?v=Z59g18awh7w
# Conceptual Video: https://www.youtube.com/watch?v=Wyv0ZU8ilCM
# ------------------------------------------------------------------------------

class BullsAndCowsGame:
    """Encapsulates the Bulls and Cows game state and AI helper.

    Attributes:
        all_combinations (list[tuple[int]]): All 4-digit permutations (0-9).
        candidates (list[tuple[int]]): Remaining possible secrets consistent
            with feedback received so far.
        secret (tuple[int] | None): The secret chosen for the current game.
        history (list): Optional placeholder for past guesses/feedback.
    """

    def __init__(self):
        # Generate all valid 4-digit numbers with unique digits (5040 total)
        self.all_combinations = list(itertools.permutations(range(10), 4))
        self.candidates = self.all_combinations.copy()
        self.secret = None
        self.history = []

    def generate_secret(self):
        """Selects a random secret from valid combinations."""
        self.secret = random.choice(self.all_combinations)
        return self.secret

    def get_feedback(self, secret, guess):
        """
        Calculates Bulls (exact position) and Cows (wrong position).
        Args:
            secret (tuple): The target number (e.g., (1, 2, 3, 4))
            guess (tuple): The guess to evaluate
        Returns:
            tuple: (bulls, cows)
        """
        bulls = sum(s == g for s, g in zip(secret, guess))
        # Cows: count common digits, subtract bulls
        common_digits = len(set(secret) & set(guess))
        cows = common_digits - bulls
        return bulls, cows

    def calculate_uncertainty(self):
        """
        Calculates the entropy (uncertainty) of the CURRENT state.
        This is log2 of the size of the remaining candidate pool.
        """
        pool_size = len(self.candidates)
        if pool_size == 0:
            return 0.0
        return math.log2(pool_size)

    def calculate_guess_entropy(self, guess, candidates):
        """
        Calculates the Expected Entropy (Information Value) of a specific guess.
        
        Formula: H(guess) = - Sum( P(outcome) * log2(P(outcome)) )
        where outcome is a specific (bulls, cows) pair.
        """
        # Collect feedback outcomes for all possible secrets; this builds the
        # distribution of (bulls,cows) outcomes we will use to compute entropy.
        outcomes = []
        
        # Simulate this guess against ALL currently possible secrets
        for possible_secret in candidates:
            feedback = self.get_feedback(possible_secret, guess)
            outcomes.append(feedback)
        
        # Count occurrences of each feedback pattern (e.g., how many secrets give 1B2C?)
        counts = Counter(outcomes)
        total = len(candidates)
        
        entropy = 0.0
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
            
        return entropy

    def suggest_best_guess(self):
        """
        Strategy: Find the guess that maximizes Expected Entropy.
        (Minimizes the expected size of the remaining pool).
        """
        # Optimization: If pool is small, check all. If large, checking 5040x5040 is slow.
        # For the first guess, '0123' is mathematically known to be optimal/near-optimal.
        if len(self.candidates) == 5040:
            return (0, 1, 2, 3) # Return immediately to save time on first turn as it will be takes a longer to iterate on whole pool.

        best_guess = None
        max_entropy = -1.0

        # We search through valid candidates (Consistent Heuristic)
        # Note: A true Minimax searches the whole space, but searching candidates is faster 
        search_space = self.candidates 

        # Evaluate candidate guesses and pick the one with max expected entropy
        print(f"    [AI is thinking... scanning {len(search_space)} candidates]")
        
        for guess in search_space:
            h = self.calculate_guess_entropy(guess, self.candidates)
 
            if h > max_entropy:
                max_entropy = h
                best_guess = guess
        
        return best_guess

    def filter_candidates(self, guess, actual_feedback):
        """Removes candidates that wouldn't produce the observed feedback."""
        self.candidates = [
            c for c in self.candidates 
            if self.get_feedback(c, guess) == actual_feedback
        ]

    def parse_input(self, user_input):
        """Validates user input."""
        if len(user_input) != 4 or not user_input.isdigit():
            return None
        digits = tuple(int(d) for d in user_input)
        if len(set(digits)) != 4:
            return None
        return digits

    def play(self):
        print("=========================================")
        print("   BULLS AND COWS: ENTROPY EDITION")
        print("=========================================")
        print("Rules: Guess the 4-digit number (unique digits).")
        print("Goal: Minimize uncertainty (Entropy) to 0 bits.")
        
        # Choose the secret for this playthrough (hidden from the player)
        self.generate_secret()
        attempts = 0
        
        while True:
            # 1. Display Current Uncertainty
            uncertainty = self.calculate_uncertainty()
            print(f"\n--- Turn {attempts + 1} ---")
            print(f"Current State Entropy (Uncertainty): {uncertainty:.4f} bits")
            print(f"Remaining possible numbers: {len(self.candidates)}")

            # 2. Offer AI Hint (Part 2 of assignment)
            ask_ai = input("Would you like an Entropy-based AI hint? (y/n): ").lower()
            if ask_ai.startswith('y'):
                # Show the AI's recommended guess (one that maximizes expected entropy)
                best_move = self.suggest_best_guess()
                print(f"Recommended Guess (Max Entropy): {''.join(map(str, best_move))}")

            # 3. User Guess
            user_input = input("Enter your guess: ")
            guess = self.parse_input(user_input)
            
            if not guess:
                print("Invalid input! Must be 4 unique digits.")
                continue

            attempts += 1
            
            # 4. Feedback
            bulls, cows = self.get_feedback(self.secret, guess)
            print(f"Result: {bulls} Bulls, {cows} Cows")
            
            if bulls == 4:
                print(f"\nCONGRATULATIONS! You found the secret {''.join(map(str, self.secret))}.")
                print(f"Total guesses: {attempts}")
                break
            
            # 5. Update Entropy State (Filter Candidates)
            prev_count = len(self.candidates)
            self.filter_candidates(guess, (bulls, cows))
            
            # Show information gain
            if len(self.candidates) > 0:
                new_uncertainty = self.calculate_uncertainty()
                print(f"Information Gained: {uncertainty - new_uncertainty:.4f} bits")
            else:
                print("Error: No candidates remaining. Did you make a mistake?")
                break

if __name__ == "__main__":
    # Main Game start from here
    game = BullsAndCowsGame()
    game.play()