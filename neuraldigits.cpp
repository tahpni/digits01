#include <iostream>
#include <ios>
#include <vector>
#include <random>
#include <cmath>
#include <cstdlib>
#include <ctime>

// Sigmoid activation function to fix output between 0 and 1
double sigmoid(double x)
{
  return 1.0 / (1.0 + exp(-x));
}

class Neuron
{
  // Public is used instead of struct because thats how people do it lol
  public:
    // Initialize program output, bias, and weights.
    double output;
    double bias;
    std::vector<double> weights;

    // Create random neurons for the data to train off of
    Neuron(int inputs)
    {
      bias = 0;
      for (int i = 0; i < inputs; ++i)
      {
        // Append to each weight
        weights.push_back(0);
      }
        
    }
    // create a way to calculate the output of each vector
    // use a constant reference because its faster than copying the whole thing, like malan said
    double CalcOutput(const std::vector<double>& inputs)
    { 
      double sum = 0.0;
      size_t i = 0;
      for (i = 0; i < inputs.size(); ++i) 
      {
        sum += inputs[i] * weights[i];
      }
      output = sigmoid(sum + bias);
      return output;
    }
};
    
int main ()
{
    const unsigned char image_data[] =
    {
        Userinput = UserInput.png
    };
    printf("Hello World");
}
