#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

int main(void) 
{
    std::ifstream file("image_path.txt");
    if (!file.is_open()) 
    {
        return 1;
    }

    std::string imagePath;
    std::getline(file, imagePath);
    file.close();

    std::cout << "Image path: " << imagePath << std::endl;

    // You can add code here to process the image using the path

    return 0;
}
