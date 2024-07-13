#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <random>

std::vector<double> softmax(const std::vector<double>& z) {
    std::vector<double> result(z.size());
    double sum_exp = 0.0;
    for (size_t i = 0; i < z.size(); ++i) {
        sum_exp += exp(z[i]);
    }
    for (size_t i = 0; i < z.size(); ++i) {
        result[i] = exp(z[i]) / sum_exp;
    }
    return result;
}

class Neuron {
public:
    double bias;
    std::vector<double> weights;

    Neuron(int inputs) {
        bias = 0.0;
        std::random_device rd;
        std::mt19937 gen(rd());
        std::normal_distribution<> d(0, 1);

        for (int i = 0; i < inputs; ++i) {
            weights.push_back(d(gen) * 0.01);
        }
    }

    double CalcOutput(const std::vector<double>& inputs) const {
        double sum = 0.0;
        for (size_t i = 0; i < inputs.size(); ++i) {
            sum += inputs[i] * weights[i];
        }
        return sum + bias;
    }

    void updateWeights(const std::vector<double>& inputs, double gradient, double learning_rate) {
        for (size_t i = 0; i < weights.size(); ++i) {
            weights[i] -= learning_rate * gradient * inputs[i];
        }
        bias -= learning_rate * gradient;
    }
};

bool parseCSV(const std::string& filename, std::vector<std::vector<double> >& data, std::vector<int>& labels) {
    std::ifstream inputfile(filename);
    if (!inputfile) {
        std::cerr << "The file does not exist." << std::endl;
        return false;
    }
    std::string line;
    getline(inputfile, line);
    while (getline(inputfile, line)) {
        std::stringstream ss(line);
        std::string token;
        std::vector<double> tempData;
        getline(ss, token, ',');
        labels.push_back(std::stoi(token));
        while (getline(ss, token, ',')) {
            tempData.push_back(std::stod(token) / 255.0);
        }
        data.push_back(tempData);
    }
    return true;
}

bool loadTestData(const std::string& filename, std::vector<double>& inputs) {
    std::ifstream inputfile(filename);
    if (!inputfile) {
        std::cerr << "The file does not exist." << std::endl;
        return false;
    }
    std::string line;
    while (getline(inputfile, line)) {
        std::stringstream ss(line);
        std::string token;
        while (getline(ss, token, ',')) {
            inputs.push_back(std::stod(token) / 255.0);
        }
    }
    return true;
}

double crossEntropyLoss(const std::vector<double>& predicted, int label) {
    return -log(predicted[label]);
}

void train(std::vector<Neuron>& neurons, const std::vector<std::vector<double> >& X, const std::vector<int>& y, double learning_rate, int epochs) {
    int m = X.size();
    int num_classes = neurons.size();

    for (int epoch = 0; epoch < epochs; ++epoch) {
        double total_loss = 0.0;
        for (int i = 0; i < m; ++i) {
            std::vector<double> outputs;
            for (size_t j = 0; j < neurons.size(); ++j) {
                outputs.push_back(neurons[j].CalcOutput(X[i]));
            }
            std::vector<double> probabilities = softmax(outputs);
            total_loss += crossEntropyLoss(probabilities, y[i]);
            for (size_t j = 0; j < neurons.size(); ++j) {
                double error = probabilities[j] - (y[i] == static_cast<int>(j));
                neurons[j].updateWeights(X[i], error, learning_rate);
            }
        }
    }
}

int main() {
    std::vector<double> inputs;
    if (!loadTestData("test.csv", inputs)) {
        return -1;
    }

    std::vector<std::vector<double> > X;
    std::vector<int> y;
    if (!parseCSV("train.csv", X, y)) {
        return -1;
    }

    // Parameters
    int num_classes = 10;
    int input_size = 784;
    double learning_rate = 0.01;
    int epochs = 10;

    if (inputs.size() != input_size) {
        std::cerr << "I'll try to run it anyway, but the input size should be " << input_size << " and it's this: " << inputs.size() << std::endl;
    }

    std::vector<Neuron> neurons;
    for (int i = 0; i < num_classes; ++i) {
        neurons.push_back(Neuron(input_size));
    }

    train(neurons, X, y, learning_rate, epochs);

    std::vector<double> outputs;
    for (size_t i = 0; i < neurons.size(); ++i) {
        outputs.push_back(neurons[i].CalcOutput(inputs));
    }

    std::vector<double> probabilities = softmax(outputs);

    int predicted_class = std::distance(probabilities.begin(), std::max_element(probabilities.begin(), probabilities.end()));

    std::cout << "Your number is " << predicted_class << std::endl;
    return 0;
}
