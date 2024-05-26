# -*- coding: utf-8 -*-
"""Triglyceride levels.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QDcWoz2j4zrqv42dU9BSFBKdDzYfaLGl
"""

# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load the training data
train_data = pd.read_csv("/content/train.csv")

# Separate features and target variable
X = train_data.drop(columns=['candidate_id', 'triglyceride_lvl'])
y = train_data['triglyceride_lvl']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing steps
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features)
    ])

# Define the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Create a pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Train the model
pipeline.fit(X_train, y_train)

# Predict on the validation set
val_predictions = pipeline.predict(X_val)

# Calculate MAE
mae = mean_absolute_error(y_val, val_predictions)
print(f'Mean Absolute Error: {mae}')

# Load the test data
test_data = pd.read_csv("/content/test.csv")

# Make predictions on the test data
test_predictions = pipeline.predict(test_data.drop(columns=['candidate_id']))

# Prepare submission file
submission_df = pd.DataFrame({'candidate_id': test_data['candidate_id'], 'triglyceride_lvl': test_predictions})

# Save submission file
submission_df.to_csv('/content/sample_submission.csv', index=False)

