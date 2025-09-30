#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int get_score(string name);
int main(void)
{
    string name1 = get_string("Player 1: ");
    string name2 = get_string("Player 2 : ");
    int score1 = get_score(name1);
    int score2 = get_score(name2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
    return 0;
}
int get_score(string name)
{
    int score = 0;
    int i = 0;
    int points[26] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                      1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    while (name[i] != '\0')
    {
        if (isalpha(name[i]))
        {
            char c = toupper(name[i]);
            score += points[c - 'A'];
        }
        i++;
    }
    return score;
}
