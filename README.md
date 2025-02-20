# Spam Detection Using SVM and SMTP

## 📌 Project Overview
This project implements **Spam Detection** using **Support Vector Machines (SVM)** and integrates **SMTP (Simple Mail Transfer Protocol)** for handling email communication. The goal is to classify emails as **spam or non-spam** based on their content and efficiently manage email transactions.

## 🚀 Features
- **Email Classification using SVM**: Trains an SVM model to differentiate spam and non-spam emails.
- **Email Preprocessing**: Tokenization, stopword removal, stemming, and TF-IDF feature extraction.
- **SMTP Integration**: Sends email notifications for detected spam or important messages.
- **Logging & Reporting**: Keeps a record of spam emails and allows users to check flagged messages.

## 📂 Project Structure
```
📁 SpamDetection-SVM-SMTP/
│── Datasets/                  # Dataset containing spam & non-spam emails
│── Datasets/spam.csv
│── CODE
│── CODE/📜 client.py              # Client end
│── CODE/📜 email.txt              # Predict if an email is spam or not
│── CODE/📜 server.py              # Server end
│── CODE/📜 svm_model.py           # Model 
│── 📜 README.md              # Project documentation
```

## 🛠 Installation & Setup
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Harshith422/SpamDetection-SVM-SMTP.git
   cd SpamDetection-SVM-SMTP
   ```
2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up SMTP Email Configuration**  
   Update `smtp_handler.py` with your SMTP credentials.
   ```python
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
   EMAIL_USER = "your-email@gmail.com"
   EMAIL_PASS = "your-password"
   ```

## 🎯 Usage
- **Train the Model**  
  ```bash
  svm_model.py
  ```
- **Classify an Email**  
  ```bash
  email.txt --email "example_email.txt"
  ```
- **Send Email Alerts via SMTP**  
  ```bash
  python client.py --recipient "user@example.com" --subject "Spam Alert" --message "Spam detected!"
  ```

## 🧠 Model & Approach
- **Support Vector Machine (SVM)** is used for text classification.
- **TF-IDF (Term Frequency-Inverse Document Frequency)** is applied to convert text into numerical features.
- **Email Handling with SMTP** to automate email responses.

## 🔥 Future Enhancements
- Implement deep learning models like LSTMs or Transformers.
- Add a web interface for email classification.
- Automate spam reporting to email providers.
