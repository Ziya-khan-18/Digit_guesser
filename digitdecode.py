import random as r
import time as t

def display_level_info(level_num, length, guess_limit,
                       has_lifeline, repeatable, highscore, timelimit):
    print(f"\nLevel {level_num} Details:")
    print(f"- Length: {length} digits")
    print(f"- Guess limit: {'Unlimited' if guess_limit is None else guess_limit}")
    print(f"- Lifeline available: {'Yes' if has_lifeline else 'No'}")
    print(f"- Repeatable digits: {'Yes' if repeatable else 'No'}")
    print(f"- Highscore tracking: {'Yes' if highscore else 'No'}")
    print(f"- Time limit: {'None' if timelimit is None else f'{timelimit} minutes'}")

def get_valid_input(prompt):
    while True:
        value = input(prompt)
        if value.lower() in ['q', 'quit']:
            return None
        if not value.isdigit():
            print("\nPlease enter a valid number")
            continue
        num = int(value)
        return num

def get_yes_no_input(prompt):
    while True:
        choice = input(prompt).lower()
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        print("\nPlease enter 'yes' or 'no'")

def matches(userinput, computer, level_length):
    exact_matches = 0
    used_positions = set()
    computer_freq = {}
    user_freq = {}
    for i in range(level_length):
        if computer[i] == userinput[i]:
            exact_matches += 1
            used_positions.add(i)
        else:
            computer_freq[computer[i]] = computer_freq.get(computer[i], 0) + 1
            user_freq[userinput[i]] = user_freq.get(userinput[i], 0) + 1
    partial_matches = 0
    for digit in computer_freq:
        if digit in user_freq:
            partial_matches += min(computer_freq[digit], user_freq[digit])
    return [exact_matches, partial_matches]

def userinput(level_length, repeatable):
    while True:
        num = input(f"Guess a unique {level_length} digit number (or 'q' to quit): ")
        if num.lower() in ['q', 'quit']:
            return None
        if num.isdigit():
            if len(num) == level_length:
                if not repeatable:
                    if len(set(num)) == level_length:
                        return num
                    else:
                        print('\nNot a unique number, try again, no digits can repeat')
                else:
                    return num
            else:
                print(f"\nNot a {level_length} digit number")
        else:
            print('\nNot a number, retry')

def computer(level_length, repeatable):
    first_digit = str(r.randint(1, 9))
    remaining_digits = ''.join([str(r.randint(0, 9)) for _ in range(level_length - 1)])
    random_num_str = first_digit + remaining_digits
    if not repeatable:
        return checker(random_num_str, level_length, repeatable)
    else:
        return random_num_str

def checker(random_num_str, level_length, repeatable):
    if len(set(random_num_str)) == level_length:
        return random_num_str
    else:
        return computer(level_length, repeatable)

def guesschecker(level_length, random_num, guess_count_remain, has_lifeline, repeatable, highscore, timelimit):
    guess_count = 0
    flag_used = False
    start_time = t.time()
    while guess_count_remain is None or guess_count < guess_count_remain:
        if timelimit:
            elapsed_time = t.time() - start_time
            remaining_time = timelimit * 60 - elapsed_time
            if remaining_time <= 0:
                print("\nTime's up! You ran out of time!")
                print('\nThe number was: ',random_num)
                return None
            print(f"\nTime remaining: {int(remaining_time // 60)} minutes, {int(remaining_time % 60)} seconds")
        if timelimit and remaining_time <= 0:
            print("\nTime's up! You cannot guess anymore.")
            print('\nThe number was: ',random_num)
            return None
        user_guess = userinput(level_length, repeatable)
        if user_guess is None:
            print("\nQuitting level...")
            return None
        result = matches(user_guess, random_num, level_length)
        guess_count += 1
        if result[0] == level_length:
            print(f"\nCongratulations! You've decoded the secret code in {guess_count} attempts: {random_num}.")
            return guess_count
        print(f"\nFeedback: {result[0]} digits at right place, {result[1]} digits at wrong place.")
        if has_lifeline and not flag_used:
            if get_yes_no_input("\nDo you wish to use a lifeline? (yes/no): "):
                lifeline_hint = use_lifeline(random_num)
                print(f"\nLifeline used: {lifeline_hint[0]} is at position {lifeline_hint[1] + 1}")
                flag_used = True
            else:
                print("\nNo lifeline used. It's there if you want.")
        elif has_lifeline and flag_used:
            print("\nNo lifelines left.")
            print(f"Lifeline previously used: {lifeline_hint[0]} is at position {lifeline_hint[1] + 1}")
        else:
            print("\nNo lifelines available.")
        if guess_count_remain is not None:
            print(f"\nGuesses remaining: {guess_count_remain - guess_count}")
    print("\nOops! You ran out of guesses!")
    print('\nThe number was: ',random_num)
    return None

def ask_retry():
    return get_yes_no_input("\nWould you like to retry this level? (yes/no): ")

def ask_quit():
    if get_yes_no_input("\nDo you wish to quit? (yes/no): "):
        print("\nThanks for playing!")
        quit()

def use_lifeline(random_num):
    index_value = r.randint(0, len(random_num) - 1)
    return random_num[index_value], index_value

def play_level(level_num, level_length, guess_limit=None, has_lifeline=False, repeatable=False, highscore=False, timelimit=None):
    best_guess_count = None
    while True:
        print(f"\nLevel {level_num}")
        random_num = computer(level_length, repeatable)
        guess_count = guesschecker(level_length, random_num, guess_limit, has_lifeline, repeatable, highscore, timelimit)
        if guess_count is not None:
            if best_guess_count is None or guess_count < best_guess_count:
                best_guess_count = guess_count
        if not highscore or not ask_retry():
            break
    if highscore and best_guess_count is not None:
        print(f"\nBest score for this level: {best_guess_count} guesses.")
    return best_guess_count is not None

def create_custom_level():
    print("\nCustom Level Builder (enter 'q' or 'quit' to return to menu)")
    length = get_valid_input("\nEnter number of digits: ")
    if length is None:
        return None
    has_guess_limit = get_yes_no_input("\nDo you want a guess limit? (yes/no): ")
    guess_limit = None
    if has_guess_limit:
        guess_limit = get_valid_input("\nEnter guess limit: ")
        if guess_limit is None:
            return None
    has_lifeline = get_yes_no_input("\nInclude lifeline? (yes/no): ")
    repeatable = get_yes_no_input("\nAllow repeatable digits? (yes/no): ")
    highscore = get_yes_no_input("\nEnable highscore tracking? (yes/no): ")
    has_timelimit = get_yes_no_input("\nDo you want a time limit? (yes/no): ")
    timelimit = None
    if has_timelimit:
        timelimit = get_valid_input("\nEnter time limit in minutes: ")
        if timelimit is None:
            return None
    return (9, length, guess_limit, has_lifeline, repeatable, highscore, timelimit)

def select_level(levels):
    while True:
        print("\nSelect a level:")
        print("1. Story Mode (play through preset levels)")
        print("2. Custom Level")
        print("3. Level Select")
        print("4. Quit")
        choice = input("\nEnter your choice (1-4): ")
        if choice == '1':
            return "story"
        elif choice == '2':
            custom_level = create_custom_level()
            if custom_level:
                return custom_level
            continue
        elif choice == '3':
            print("\nAvailable Levels:")
            for i, (level_num, length, guess_limit, has_lifeline, repeatable, highscore, timelimit) in enumerate(levels, 1):
                print(f"\nLevel {level_num}:")
                display_level_info(level_num, length, guess_limit, has_lifeline, repeatable, highscore, timelimit)
            level_choice = get_valid_input(f"\nSelect level (1-{len(levels)}): ")
            if level_choice is None:
                continue
            if 1 <= level_choice <= len(levels):
                return levels[level_choice - 1]
            else:
                print("\nInvalid level number.")
        elif choice == '4':
            return None
        else:
            print("\nInvalid choice. Please try again.")

def play_game():
    levels = [
        (1, 4, None, False, False, False, None),
        (2, 4, 7, False, False, False, None),
        (3, 4, 6, True, False, False, None),
        (4, 5, None, False, False, False, None),
        (5, 4, None, False, True, False, None),
        (6, 4, None, False, False, True, None),
        (7, 4, 7, False, False, False, 3),
        (8, 10, 20, True, True, True, 10)
    ]
    print("-------Welcome to the Number Guessing Game!-------\n")
    while True:
        selection = select_level(levels)
        if selection is None:
            print("\nThanks for playing!")
            break
        elif selection == "story":
            print("\n--- Starting Story Mode ---")
            all_levels_cleared = True
            for level_data in levels:
                level_num, length, guess_limit, has_lifeline, repeatable, highscore, timelimit = level_data
                display_level_info(level_num, length, guess_limit, has_lifeline, repeatable, highscore, timelimit)
                success = play_level(level_num, length, guess_limit, has_lifeline, repeatable, highscore, timelimit)
                if not success:
                    print(f"\nYou failed Level {level_num}. Story Mode over.")
                    all_levels_cleared = False
                    break
                if level_num < len(levels):
                    if not get_yes_no_input("\nLevel complete! Continue to the next level? (yes/no): "):
                        all_levels_cleared = False
                        break
            if all_levels_cleared:
                print("\nCongratulations! You've completed all levels in Story Mode!")
            if not get_yes_no_input("\nReturn to main menu? (yes/no): "):
                print("\nThanks for playing!")
                break
        elif isinstance(selection, tuple):
            level_num, length, guess_limit, has_lifeline, repeatable, highscore, timelimit = selection
            display_level_info(level_num, length, guess_limit, has_lifeline, repeatable, highscore, timelimit)
            play_level(level_num, length, guess_limit, has_lifeline, repeatable, highscore, timelimit)
            if not get_yes_no_input("\nWould you like to try another level? (yes/no): "):
                print("\nThanks for playing!")
                break

if __name__ == "__main__":
    play_game()