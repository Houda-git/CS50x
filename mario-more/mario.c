#include <cs50.h>
#include <stdio.h>

void print_wall(int i, int max);

int main(void)
// Print mario walls
{
    int number;
    do
    {
        number = get_int("Give me a number between 1 and 8 included: ");
    }
    while (number < 1 || number > 8);

    for (int i = 1; i < number + 1; i++)
    {
        print_wall(i, number);
    }
}
void print_wall(int num, int max)
// Figure out how to create bricks
{
    for (int i = 0; i < max - num; i++)
    {
        printf(" ");
    }
    for (int i = max - num; i < max; i++)
    {
        printf("#");
    }
    printf("  ");
    for (int i = 0; i < num; i++)
    {
        printf("#");
    }
    printf("\n");
}
