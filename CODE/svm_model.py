# Import necessary libraries
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

# Define a SimpleSVM class
class SimpleSVM:
    def __init__(self, learning_rate=0.01, epochs=1000):
        # Initialize the SVM model with specified learning rate and epochs
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None  # Weight vector
        self.bias = None  # Bias term

    def fit(self, X, y):
        # Convert labels to -1 (negative class) and 1 (positive class)
        y = np.where(y == 'spam', 1, -1)

        # Initialize weights and bias to zeros
        self.weights = np.zeros(X.shape[1])
        self.bias = 0

        # Gradient Descent
        for epoch in range(self.epochs):
            for i in range(X.shape[0]):
                # Check if the example is inside the margin
                if y[i] * (np.dot(X[i], self.weights) + self.bias) <= 1:
                    # Update weights and bias using gradient descent
                    self.weights += self.learning_rate * (y[i] * X[i] - 2 * (1/self.epochs) * self.weights)
                    self.bias += self.learning_rate * y[i]

    def predict(self, X):
        # Predict class labels using the learned weights and bias
        return np.sign(np.dot(X, self.weights) + self.bias)

# Function to train an SVM model using input data and labels
def train_svm_model(train_data, train_labels, vectorizer):
    # Apply the CountVectorizer to the training data
    X_train = vectorizer.transform(train_data)

    # Create a SimpleSVM model and train it
    svm_model = SimpleSVM()
    svm_model.fit(X_train.toarray(), train_labels)
    return svm_model

# Function to classify an email using the trained SVM model
def classify_email(model, email_content, vectorizer):
    # Apply the CountVectorizer to the email content
    X_email = vectorizer.transform([email_content]).toarray()

    # Predict using the SimpleSVM model
    prediction = model.predict(X_email)
    return bool(prediction[0] == 1)
