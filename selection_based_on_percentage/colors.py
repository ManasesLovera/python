import random

class ColorSelection:

    def __init__(self, color_a_percentage: int):
        """
        Initializes the selection with a percentage for color A.
        Color B's percentage is automatically set to (100 - color_a_percentage).
        """
        self.set_color_a_percentage(color_a_percentage)

    def set_color_a_percentage(self, percentage: int):
        """
        Sets the probability of selecting color A.
        Ensures the percentage is between 0 and 100.
        """
        if 0 <= percentage <= 100:
            self.color_a_percentage = percentage
            self.color_b_percentage = 100 - percentage
        else:
            raise ValueError("Percentage must be between 0 and 100")
        
    def get_color(self):
        """
        Randomly selects a color based on the set probability.
        """
        return "Color A" if random.randint(1, 100) <= self.color_a_percentage else "Color B"
    
# Example Usage
color_selector = ColorSelection(75) # 75% Color A, 25% Color B

# Simulate multiple selections to verify probability distribution
selection_results = {"Color A": 0, "Color B": 0}
num_trials = 1000

for _ in range(num_trials):
    selected_color = color_selector.get_color()
    selection_results[selected_color] += 1

# Display results
selection_results

# Example Output
# > {'Color A': 758, 'Color B': 242}