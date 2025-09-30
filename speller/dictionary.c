// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Hashes word to a number
// I use here the algorithm of djb2, created by Daniel J. Bernstein
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + tolower(c); // hash * 33 + c
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
unsigned int size_word = 0;
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Failed to open the file");
        return false;
    }
    char mot[LENGTH + 1];
    while (fscanf(file, "%s", mot) != EOF) // We read word by word
    {
        node *new_node = malloc(sizeof(node)); // Go to the place where we will store the word
        if (new_node == NULL)
        {
            fclose(file);
            return false;
        }
        int i = 0;
        strcpy(new_node->word, mot);
        const int index = hash(mot);
        new_node->next = table[index];
        table[index] = new_node;
        size_word++;
    }
    fclose(file);
    return true;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int index = hash(word);
    node *words = table[index];
    while (words != NULL)
    {
        if (strcasecmp(words->word, word) == 0)
        {
            return true;
        }
        words = words->next;
    }
    return false;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return size_word;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *word = table[i];
        while (word != NULL)
        {
            node *temp = word->next;
            free(word);
            word = temp;
        }
    }
    return true;
}
