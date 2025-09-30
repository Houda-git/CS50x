#include <cs50.h>
#include <stdio.h>

int main(void)
// Ask for your name and greet you
{
    string name = get_string("What's your name? ");
    printf("hello, %s\n", name);
}
