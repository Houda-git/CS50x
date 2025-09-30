#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            RGBTRIPLE pixel = image[h][w];
            int red = pixel.rgbtRed;
            int green = pixel.rgbtGreen;
            int blue = pixel.rgbtBlue;
            int average = (int) ((red + green + blue) / 3.0 + 0.5);
            image[h][w].rgbtRed = average;
            image[h][w].rgbtGreen = average;
            image[h][w].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int middle = width / 2;
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < middle; w++)
        {
            RGBTRIPLE temp = image[h][w];
            image[h][w] = image[h][width - w - 1];
            image[h][width - w - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int directions[3] = {-1, 0, 1};
    // Copy the original image
    RGBTRIPLE copy[height][width];
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            copy[h][w] = image[h][w];
        }
    }

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            // for each pixel we are here in the pixel image[h][w]
            int average_red = 0;
            int average_green = 0;
            int average_blue = 0;
            int count = 0;
            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    int dh = h + directions[i];
                    int dw = w + directions[j];
                    if (dh >= 0 && dh < height && dw >= 0 && dw < width)
                    {
                        average_red += copy[dh][dw].rgbtRed;
                        average_green += copy[dh][dw].rgbtGreen;
                        average_blue += copy[dh][dw].rgbtBlue;
                        count++;
                    }
                }
            }
            average_red = round((float) average_red / count);
            average_green = round((float) average_green / count);
            average_blue = round((float) average_blue / count);
            image[h][w].rgbtRed = average_red;
            image[h][w].rgbtGreen = average_green;
            image[h][w].rgbtBlue = average_blue;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int directions[3] = {-1, 0, 1};
    int gx[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int gy[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    // Copy the original image
    RGBTRIPLE copy[height][width];
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            copy[h][w] = image[h][w];
        }
    }

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            // for each pixel we are here in the pixel image[h][w]
            int gx_red = 0;
            int gx_green = 0;
            int gx_blue = 0;
            int gy_red = 0;
            int gy_green = 0;
            int gy_blue = 0;
            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    int dh = h + directions[i];
                    int dw = w + directions[j];
                    if (dh >= 0 && dh < height && dw >= 0 && dw < width)
                    {
                        gx_red += copy[dh][dw].rgbtRed * gx[i * 3 + j];
                        gx_green += copy[dh][dw].rgbtGreen * gx[i * 3 + j];
                        gx_blue += copy[dh][dw].rgbtBlue * gx[i * 3 + j];
                        gy_red += copy[dh][dw].rgbtRed * gy[i * 3 + j];
                        gy_green += copy[dh][dw].rgbtGreen * gy[i * 3 + j];
                        gy_blue += copy[dh][dw].rgbtBlue * gy[i * 3 + j];
                    }
                }
            }
            int average_red = round(sqrt(gx_red * gx_red + gy_red * gy_red));
            int average_green = round(sqrt(gx_green * gx_green + gy_green * gy_green));
            int average_blue = round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));
            image[h][w].rgbtRed = average_red > 255 ? 255 : average_red;
            image[h][w].rgbtGreen = average_green > 255 ? 255 : average_green;
            image[h][w].rgbtBlue = average_blue > 255 ? 255 : average_blue;
        }
    }
    return;
}
