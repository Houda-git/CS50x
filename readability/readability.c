#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

float get_letters(string text, int words);
float get_sentences(string text, int words);
int get_words(string text);

int main(void)
{
    // Coleman-Liau index
    string text = get_string("Text : ");
    int words = get_words(text);
    float L = get_letters(text, words);
    float S = get_sentences(text, words);
    float index;
    index = 0.0588 * L - 0.296 * S - 15.8;
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", (int) (index + 0.5));
    }
    return 0;
}
int get_words(string text)
{
    // Return the number of words we have in the text
    int words = 1;
    int i = 0;
    while (text[i] != '\0')
    {
        if (text[i] == ' ')
        {
            words++;
        }
        i++;
    }
    return words;
}
float get_letters(string text, int words)
{
    // Return the number of letters per 100 words
    int num_letters = 0;
    int i = 0;
    while (text[i] != '\0')
    {
        if (isalpha(text[i]))
        {
            num_letters++;
        }
        i++;
    }
    return (num_letters * 100.0) / words;
}

float get_sentences(string text, int words)
{
    // Return the number of sentences per 100 words
    int num_sentences = 0;
    int i = 0;
    while (text[i] != '\0')
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            num_sentences++;
        }
        i++;
    }
    return (num_sentences * 100.0) / words;
}
