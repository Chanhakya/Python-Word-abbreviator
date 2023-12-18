import numpy as np #installing libraries
def File_reader(filepath_values): # Function to read values from the specified file and return a sorted values dictionary.
    # Lists to store letters and values
    letters = []
    values = []
    # Reads values from the file
    with open(filepath_values) as file:
        for line in file:
            # Splits each line and extracts letters by removing trailing whitespaces 
            letters.append(line.rstrip().split()[0])
            # Appends the obtained integral part to the values list
            values.append(int(line.rstrip().split()[1]))
    # Creating a dictionary mapping letters to values
    Mapped_dict = dict(zip(letters, values))
    # Sort the dictionary based on values
    sorted_dict = dict(sorted(Mapped_dict.items(), key=lambda x: x[1]))
    # Returns the sorted values dictionary
    return sorted_dict
def least_valued_letter_func(Text, sorted_dict):
    # Function to check the least letter in a word
    # Initializes variables to keep track of the least letter and its score
    least_letter = None
    least_valued_letter = float('inf')  # Initialize with positive infinity as a placeholder
    index_count = 0
    # Iterates through each letter in the word
    for letter in Text[1:]:
        index_count += 1
        # Checking if the letter is in sorted_dict before accessing its value
        if letter in sorted_dict:
            current_letter_score = sorted_dict[letter]     
            if current_letter_score < least_valued_letter or least_letter is None:
                least_letter = letter
                least_valued_letter = current_letter_score + (index_count if index_count <= 2 else 3)
                if least_letter == Text[-1]:
                    for inner_letter in Text[1:-1]:
                        if inner_letter in sorted_dict and sorted_dict[inner_letter] < 5:
                            least_letter = inner_letter
                            least_valued_letter = sorted_dict[inner_letter] + (index_count if index_count <= 2 else 3)
                elif sorted_dict.get(least_letter, 0) > 5 and Text[-1] != 'E':
                    least_letter = Text[-1]
                    least_valued_letter = 5
                elif sorted_dict.get(least_letter, 0) > 20 and Text[-1] == 'E':
                    least_letter = Text[-1]
                    least_valued_letter = 20
                else:
                    least_valued_letter = sorted_dict.get(letter, 0) + (index_count if index_count <= 2 else 3)
    return least_letter, least_valued_letter, index_count
def score_checker(word, sorted_dict):
# Function to check the least valued letters and scores for each word in 'word'
    index_count = 0
    least_letter_tracker = {} # Dictionary to track the least valued letter for each word
    least_score_tracker = {}  # Dictionary to track the score for each word
    words_split = word.split()
    for Text in words_split: 
        least_letter, least_valued_letter, index_count = least_valued_letter_func(Text, sorted_dict)
        # Updating the dictionaries with the results for the current word
        least_score_tracker[Text] = least_valued_letter
        least_letter_tracker[Text] = least_letter
    return least_letter_tracker, least_score_tracker
def abbreviator(word, sorted_dict):  
    #Generate AON (Abbreviation) and score for a given word.
    #param word: The input word.
    #param sorted_dict: A dictionary containing sorted values for letters.
    #return: A tuple containing AON and score
    AON = ''  # AON is least scored abbreviation for abbreviation
    final_score = -1
    words = word.split()
    if len(words) == 1:
        # For single-word input
        single_word = words[0]
        if len(single_word) < 3:
            AON = ''
            final_score = np.nan
        elif len(single_word) == 3:
            AON = single_word
            mid_letter_score = sorted_dict[single_word[1]]
            final_score = mid_letter_score + 20 if AON[-1] == 'E' else mid_letter_score + 5
        elif len(single_word) > 3:
            AON = single_word[0]
            least_letter, least_letter_score, least_index_count = least_valued_letter_func(single_word, sorted_dict)
            if least_letter == single_word[-1]:
                second_least_letter, second_least_score, second_least_index_count = \
                    least_valued_letter_func(single_word[:-1], sorted_dict)
                AON += second_least_letter + least_letter
                final_score = least_letter_score + second_least_score
            else:
                second_least_letter, second_least_score, second_least_index_count = \
                    least_valued_letter_func(single_word.replace(least_letter, ''), sorted_dict)
                AON += second_least_letter + least_letter if second_least_index_count < least_index_count \
                    else least_letter + second_least_letter
                final_score += least_letter_score + second_least_score
    elif len(words) >= 3:
        # For multiple words
        AON = ''.join(word[0] for word in words)
    elif len(words) == 2:
        # For two words
        AON += words[0][0]
        least_letter_tracker, least_score_tracker = score_checker(word, sorted_dict)
        least_letter_word = min(least_score_tracker, key=least_score_tracker.get)
        AON += words[1][0] + least_letter_tracker[least_letter_word] if least_letter_word == words[1] \
            else least_letter_tracker[least_letter_word] + words[1][0]
        final_score = least_score_tracker[least_letter_word]
    return AON, final_score

def main():
    # Main function for processing words
    filepath_values = r'C:\Users\sarat\OneDrive\Desktop\Python Assignment\values.txt'
    # Reading values from the specified file and return a sorted values dictionary
    sorted_dict = File_reader(filepath_values)
    input_file = input("Enter the file name for abbreviations: ")
    surname = input("Enter your surname: ")
    # Create the output file name based on the input file and surname
    output_file_word = f"{surname.lower()}_{input_file[:-4]}_abbrevs.txt"
    output_file_path = output_file_word
    with open(input_file) as infile, open(output_file_path, 'w') as outfile:
        for line in infile:
            word = line.strip().upper()
            if "'" in word:
                word = word.replace("'", "")
            abbrev, score = abbreviator(word, sorted_dict)
            outfile.write(word + '\n')
            if abbrev:
                outfile.write(abbrev + '\n')
            else:
                outfile.write('\n')

if __name__ == "__main__":
    main()