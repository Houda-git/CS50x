#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>

int main(void)
// Check the validity of a card
{
    long card = get_long("Number: ");
    long card_number = card;
    // a boolean to indicate whether we multiply by 2 or not
    bool multiply = false;
    int sum_mult = 0;
    int sum = 0;
    int length = 0;
    if (card_number == 0)
    {
        printf("INVALID\n");
        return 0;
    }
    while (card_number != 0)
    {
        if (!multiply)
        {
            int num = card_number % 10;
            sum += num;
            multiply = true;
        }
        else
        {
            int product = 2 * (card_number % 10);
            sum_mult += product / 10 + (product % 10);
            multiply = false;
        }
        card_number = card_number / 10;
        length++;
    }
    int total = sum + sum_mult;
    if (total % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    // Extract starting digits
    long starting_digits = card;
    while (starting_digits >= 100)
    {
        starting_digits /= 10;
    }
    if (length == 15 && (starting_digits == 34 || starting_digits == 37))
    {
        printf("AMEX\n");
    }
    else if ((length == 13 && starting_digits / 10 == 4) ||
             (length == 16 && starting_digits / 10 == 4))
    {
        printf("VISA\n");
    }
    else if (length == 16 && (starting_digits >= 51 && starting_digits <= 55))
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
