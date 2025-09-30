#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover file.raw");
        return 1;
    }
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("File invalid");
        return 1;
    }

    uint8_t byte[512];
    int count = 0;
    char filename[8];
    FILE *output = NULL;
    while (fread(byte, 512, 1, input) != 0)
    {
        if (byte[0] == 0xFF && byte[1] == 0xD8 && byte[2] == 0xFF &&
            (byte[3] >= 0xE0 && byte[3] <= 0xEF))
        {
            if (output != NULL) // there was an opened file
            {
                fclose(output);
            }
            sprintf(filename, "%03i.jpg", count);
            output = fopen(filename, "w");
            count++;
        }
        if (output != NULL)
        {
            fwrite(byte, 512, 1, output);
        }
    }
    if (output != NULL)
    {
        fclose(output);
    }
    fclose(input);
    return 0;
}
