import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Load preprocessed data from a file using pickle
data_dict = pickle.load(open('./data.pickle', 'rb'))

# Extract data and labels from the loaded dictionary
data = np.asarray(data_dict['data'])  # Features
labels = np.asarray(data_dict['labels'])  # Target labels

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Initialize a Random Forest classifier
model = RandomForestClassifier()

# Train the Random Forest model using the training data
model.fit(x_train, y_train)

# Use the trained model to predict labels for the test data
y_predict = model.predict(x_test)

# Calculate the accuracy of the model
score = accuracy_score(y_predict, y_test)

# Print the accuracy of the model on the test set
print('{}% of samples were classified correctly !'.format(score * 100))

# Save the trained model into a file named 'model.p' using pickle serialization
f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
