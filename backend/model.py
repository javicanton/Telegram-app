import pandas as pd
import numpy as np
import re
import nltk
import os
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, auc, confusion_matrix, precision_recall_curve, average_precision_score, accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the data
df = pd.read_csv('telegram_messages.csv')

# Text cleaning function
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove mentions and special characters
    text = re.sub(r'\@\w+|\#\w+', '', text)
    text = re.sub(r'\W', ' ', text)
    # Convert to lowercase
    text = text.lower()
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Apply the cleaning function to the 'Message Text' column
df['Cleaned_Text'] = df['Message Text'].apply(lambda x: clean_text(str(x)))

# Tokenization
df['Tokens'] = df['Cleaned_Text'].apply(lambda x: nltk.word_tokenize(x))

# Remove stopwords
stop_words = set(stopwords.words('english'))
df['Tokens'] = df['Tokens'].apply(lambda x: [word for word in x if word not in stop_words])

# Lemmatization
lemmatizer = WordNetLemmatizer()
df['Tokens'] = df['Tokens'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

# Display the processed data
print(df[['Message Text', 'Cleaned_Text', 'Tokens']].head())

# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=5000)  # Limiting to 5000 most frequent words for demonstration

# Fit and transform the cleaned text
tfidf_matrix = vectorizer.fit_transform(df['Cleaned_Text'])

# Split the data into labeled and unlabeled subsets
labeled_df = df.dropna(subset=['Label'])
unlabeled_df = df[df['Label'].isna()]

# Convert the labeled data into features and target
X_labeled = vectorizer.transform(labeled_df['Cleaned_Text'])
y_labeled = labeled_df['Label']

# Split labeled data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_labeled, y_labeled, test_size=0.2, random_state=42)

# Initialize and train the model
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)

# Predict labels for the unlabeled data
X_unlabeled = vectorizer.transform(unlabeled_df['Cleaned_Text'])
predicted_labels = logreg.predict(X_unlabeled)

# Update the unlabeled data with the predicted labels
unlabeled_df['Label_predicted'] = predicted_labels

# Combine the labeled and unlabeled data
df_updated = pd.concat([labeled_df, unlabeled_df])

# Save the updated DataFrame
df_updated.to_csv('telegram_messages_updated.csv', index=False)

# Generate predictions for the validation set
y_pred = logreg.predict(X_val)

# Calculate metrics
accuracy = accuracy_score(y_val, y_pred)
precision = precision_score(y_val, y_pred)
recall = recall_score(y_val, y_pred)
f1 = f1_score(y_val, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# Generate confusion matrix
cm = confusion_matrix(y_val, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', cbar=False)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(y_val, logreg.predict_proba(X_val)[:,1])

# Plot ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'AUC = {roc_auc_score(y_val, y_pred):.2f}')
plt.plot([0, 1], [0, 1], 'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

# Calculate precision-recall curve
precision, recall, thresholds = precision_recall_curve(y_val, logreg.predict_proba(X_val)[:,1])

# Plot precision-recall curve
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label=f'AP = {average_precision_score(y_val, y_pred):.2f}')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc='upper right')
plt.show()