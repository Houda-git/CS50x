import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print(" Usage: ./dna file.csv file.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    with open(sys.argv[1], "r") as file_csv:
        reader = csv.DictReader(file_csv)  # obtain a dictionary containing all the person's info
        database = list(reader)
        sequences = reader.fieldnames[1:]  # a dictionary containing all the sequences

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as dna_file:
        data = dna_file.read()

    # TODO: Find longest match of each STR in DNA sequence
    counts = {}
    for sequence in sequences:  # only the keys meanign by that the sequences
        max = longest_match(data, sequence)
        counts[sequence] = max
    # TODO: Check database for matching profiles
    for person in database:
        if all(counts[sequence] == int(person[sequence]) for sequence in sequences):
            print(person['name'])
            return
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
