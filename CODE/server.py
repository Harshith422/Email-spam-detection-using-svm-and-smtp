import socket
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from svm_model import train_svm_model, classify_email

# Load data from the CSV file
df = pd.read_csv('spam2.csv')

# Correcting column names to 'Category' and 'Message'
train_data, test_data, train_labels, test_labels = train_test_split(
    df['Message'], df['Category'], test_size=0.2, random_state=42
)

# Train the SVM model using the function from svm_model.py
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_data)

# Create and train the SVM model
svm_model = train_svm_model(train_data, train_labels, vectorizer)

# Server setup for receiving and sending data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12346

server_socket.bind((host, port))
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

# Variables to store correct predictions and total predictions
correct_predictions = 0
total_predictions = 0

# Function to send a message to the client
def send_message(client_socket, message):
    try:
        serialized_message = pickle.dumps(message)
        message_length = len(serialized_message).to_bytes(4, 'big')
        client_socket.sendall(message_length + serialized_message)
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

# Function to receive a message from the client
def receive_message(client_socket):
    try:
        message_length_bytes = client_socket.recv(4)
        if not message_length_bytes:
            return None

        message_length = int.from_bytes(message_length_bytes, 'big')
        received_message = b''
        while len(received_message) < message_length:
            chunk = client_socket.recv(min(1024, message_length - len(received_message)))
            if not chunk:
                return None
            received_message += chunk

        return pickle.loads(received_message)
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

# Main loop to handle client connections
while True:
    # Accept a connection from a client
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive email content from the client
    email_content = receive_message(client_socket)

    # Check if the received message is not None
    if email_content is not None:
        # Classify email as spam or not using the trained model
        result = classify_email(svm_model, email_content, vectorizer)

        # Update correct_predictions and total_predictions
        total_predictions += 1
        if result == int(test_labels.iloc[total_predictions - 1]):
            correct_predictions += 1

        # Calculate current accuracy
        current_accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0

        # Send the classification result and current accuracy back to the client
        send_message(client_socket, {'classification_result': result, 'accuracy': current_accuracy})
    else:
        print("Error: Failed to receive data from the client.")

    # Close the connection with the client
    client_socket.close()
