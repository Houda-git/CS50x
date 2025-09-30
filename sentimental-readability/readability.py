from cs50 import get_string


def main():
    text = get_string("Text: ")
    words = len(text.split())
    L = get_letters(text, words)
    S = get_sentences(text, words)
    index = 0.0588 * L - 0.296 * S - 15.8
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {int(index + 0.5)}")


def get_letters(text, length):
    sum_letters = 0
    for char in text:
        if char.isalpha():
            sum_letters += 1
    return (sum_letters * 100) / length


def get_sentences(text, length):
    sum_sentences = 0
    ending_sentences = ['?', '.', '!']
    for char in text:
        if char in ending_sentences:
            sum_sentences += 1
    return (sum_sentences * 100) / length


main()
