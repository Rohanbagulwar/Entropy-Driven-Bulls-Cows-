#  Entropy-Driven Bulls and Cows Solver 

This project implements the classic code-breaking game **Bulls and Cows**  in Python, integrating an **Information Theory** approach to measure uncertainty and guide strategy.

The core feature is the calculation of **Shannon Entropy** to quantify the information gain from every guess, allowing the player to see the mathematical uncertainty remaining in the game state.

## 🚀 Key Features

* **Standard Bulls and Cows Rules:** 4-digit secret number with unique digits (0-9).
* **Entropy Tracking:** Displays the current uncertainty (in **bits**) with every guess.
* **AI Strategy Hint:** Calculates and suggests the statistically **optimal guess**—the one that maximizes the Expected Entropy (information gain).
* **Dynamic Candidate Filtering:** Efficiently prunes the search space of 5,040 permutations based on the feedback received.

## 🔗 Deliverables & Video Links

| Deliverable | Description | Link (Placeholder - **Must be updated!**) |
| :--- | :--- | :--- |
| **Demonstration Code** | The Python game script (`BullsAndCowsgame.py`). | **https://github.com/Rohanbagulwar/Entropy-Driven-Bulls-Cows-**|
| **Demonstration Video** | Tutorial showcasing game functionality and entropy calculation (Max 5 mins). | **https://www.youtube.com/watch?v=Z59g18awh7w** |
| **Conceptual Video** | Presentation on entropy calculation, justification, and optimal strategy (Max 10 mins). | **https://www.youtube.com/watch?v=Wyv0ZU8ilCM** |

---

## 💻 Setup and Execution

### Prerequisites

You need **Python 3.12** installed on your system. No external libraries are required beyond the standard library modules (`random`, `math`, `itertools`, `collections`).

### Running the Game

1.  **Save the Code:** Save the provided Python script as `BullsAndCowsgame.py`.
2.  **Execute:** Open your terminal or command prompt, navigate to the file's directory, and run:

    ```bash
    python BullsAndCowsgame.py
    ```

3.  **Play:** Follow the on-screen prompts to enter your 4-digit guesses. The secret number is generated randomly by the computer at the start.

---

## 🧠 The Entropy Strategy Explained

The core of this project lies in the application of Information Theory to solve the game efficiently.

### 1. The Search Space

The game starts with a universe of **5,040 possible secret numbers** (permutations of 4 unique digits from 0-9). The goal is to reduce this set down to one.

### 2. Measuring Uncertainty (Entropy $H$)

* **Definition:** Entropy ($H$) is a mathematical measure of the uncertainty remaining in the system, quantified in **bits**.
* **Calculation:** The initial uncertainty is $H = \log_2(5040) \approx 12.29$ bits. This means, theoretically, we need about 12-13 perfectly efficient "Yes/No" questions to solve the game.
* **Code Function:** `calculate_uncertainty()` calculates the $\log_2$ of the current number of remaining candidate secrets.

### 3. The Optimal Strategy: Maximizing Information Gain

* **The Problem:** Which guess should we make to eliminate the most candidates, on average?
* **The Solution:** We select the guess that yields the highest **Expected Entropy** (calculated via `calculate_guess_entropy()`).
* **Logic:** A high-entropy guess ensures the remaining candidate pool is split into many small, equal-sized groups, regardless of the feedback received. This **minimizes the size of the worst-case remaining pool**, guaranteeing the fastest rate of convergence.
    * *Analogy:* It's not about being lucky; it's about forcing the game to give you the most information (bits) possible every turn, turning a game of luck into a deterministic search.

---

## 🛠️ Code Structure Overview

| Function/Variable | Description | Role in Game |
| :--- | :--- | :--- |
| `self.candidates` | List of all remaining possible secret numbers (starts at 5040). | **The Search Space.** |
| `get_feedback(secret, guess)` | Calculates the (bulls, cows) hint between two numbers. | **The Referee/Rules Engine.** |
| `calculate_uncertainty()` | Computes $\log_2(\text{len}(\text{candidates}))$. | **Displays Current Uncertainty.** |
| `calculate_guess_entropy(guess, candidates)` | Simulates a guess against all candidates to find its information value ($H$). | **The Strategy Engine.** |
| `suggest_best_guess()` | Iterates through guesses to find the one that returns the maximum expected $H$. | **The AI Hint.** |
| `filter_candidates()` | Prunes the `self.candidates` list based on the actual feedback. | **Updates the Game State (Elimination).** |