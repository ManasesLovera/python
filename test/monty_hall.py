import random

simulations = 100000
win_if_switch = 0
win_if_stay = 0

for _ in range(simulations):

    # Place the prize behind one of the 3 doors
    doors = [0, 1, 2]
    prize = random.choice(doors)

    # Player makes an initial choice
    player_choice = random.choice(doors)

    # Monty opens a door that is not the prize and not the player's choice
    remaining_doors = [door for door in doors if door != player_choice and door != prize]
    monty_opens = random.choice(remaining_doors)

    # Determine the door the player would switch to
    switch_to = [door for door in doors if door != player_choice and door != monty_opens][0]

    # Check if staying wins
    if player_choice == prize:
        win_if_stay += 1

    # Check if switching wins
    if switch_to == prize:
        win_if_switch += 1

# Print the results
print(f"Total simulations: {simulations}")
print(f"Wins if stay: {win_if_stay / simulations}")
print(f"Wins if switch: {win_if_switch / simulations}")