#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    string key = argv[1];
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characteres\n");
        return 1;
    }
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
        for (int j = i + 1; j < 26; j++)
        {
            if (toupper(key[i]) == toupper(key[j]))
            {
                printf("Key must not have the same alphabet more than once.\n");
                return 1;
            }
        }
    }
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    int i = 0;
    while (plaintext[i] != '\0')
    {
        char c = plaintext[i];
        if (isupper(c))
        {
            printf("%c", toupper(key[c - 'A']));
        }
        else if (islower(c))
        {
            printf("%c", tolower(key[c - 'a']));
        }
        else
        {
            printf("%c", c);
        }
        i++;
    }
    printf("\n");
    return 0;
}
