# Import necessary libraries
import socket
import pickle

# Function to send a message to the server
def send_message(server_socket, message):
    try:
        # Serialize the message using pickle
        serialized_message = pickle.dumps(message)
        # Convert message length to bytes and send it along with the serialized message
        message_length = len(serialized_message).to_bytes(4, 'big')
        server_socket.sendall(message_length + serialized_message)
        return True  # Return True if sending is successful
    except Exception as e:
        print(f"Error sending message: {e}")
        return False  # Return False if there's an error during sending

# Function to receive a message from the server
def receive_message(server_socket):
    try:
        # Receive the length of the message
        message_length_bytes = server_socket.recv(4)
        if not message_length_bytes:
            print("Error: No more data to receive (length).")
            return None  # No more data to receive, return None

        # Convert message length to integer
        message_length = int.from_bytes(message_length_bytes, 'big')
        received_message = b''
        while len(received_message) < message_length:
            # Receive chunks of the message
            chunk = server_socket.recv(min(1024, message_length - len(received_message)))
            if not chunk:
                print("Error: No more data to receive (chunk).")
                return None  # No more data to receive, return None
            received_message += chunk

        return pickle.loads(received_message)  # Deserialize and return the received message
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

# Function to classify an email using the server
def classify_email_with_server(email_content, server_host, server_port):
    try:
        # Establish a connection to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))

        # Send email content to the server using the send_message function
        if not send_message(client_socket, email_content):
            return None  # Exit early if sending fails

        # Receive the result from the server using the receive_message function
        result = receive_message(client_socket)

        return result  # Return the received result
    except Exception as e:
        print(f"Error during communication with the server: {e}")
        return None
    finally:
        # Close the connection in the finally block to ensure it happens regardless of exceptions
        if client_socket:
            client_socket.close()

# Example usage
# Get the path to the email file from the user
email_file_path = input("Enter the path to your email file: ")
# Read the email content from the file
with open(email_file_path, 'r') as file:
    user_email_content = file.read()

# Server details
server_host = '127.0.0.1'
server_port = 12346

# Call the classify_email_with_server function and store the result
result = classify_email_with_server(user_email_content, server_host, server_port)

# Check if the result is not None
if result is not None:
    # Check the 'classification_result' key in the result dictionary
    if result['classification_result']:
        print("The email is classified as spam.")
    else:
        print("The email is classified as not spam (ham).")
else:
    print("Error: Failed to receive data from the server.")