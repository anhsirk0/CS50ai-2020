## Experimentation Process

# I started with:
## 1 convolutional layer (32 filters, 3x3 kernel)
## 1 pooling layer (2x2 kernel)
## 1 hidden layer of 128 units and 0.5 dropout
## Output layer with NUM_CATEGORIES units
## Result: *Accuracy was less than 1 %*

# Modification made to previous layer
## added 1 more hidden layer of 128 units and 0.2 dropout
## increased number of units of 1st hidden layer (128 -> 256)
## Result: *Accuracy still less than 1 %*

# More modifications
## Gradually increased the unit size of hidden layers
## unit size of 1st layer -> 512
## unit size of 2nd layer -> 256
## Result: *Accuracy around 80%*

# Final model
## 1st hidden layer - 1024 units and 0.2 dropout
## 2nd hidden layer - 512 units and 0.2 dropout
## 3rd hidden layer - 512 units without dropout
## Training of the model took a lot of time
## Result: *Accuracy around 93%*


