import time
from sklearn.metrics import mean_absolute_percentage_error
from threading import Thread, Lock
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt


# Load the train_dataset
file_path = 'data/housing_prices_data/train.csv'
train_data = pd.read_csv(file_path, index_col="Id")

# Columns to be deleted
columns_to_delete = ['MoSold', 'YrSold', 'SaleType', 'SaleCondition', 'Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature']

# Delete the specified columns
train_data_cleaned = train_data.drop(columns=columns_to_delete, axis=1)

# Define the input features (X) and the output (y)
X = train_data_cleaned.drop('SalePrice', axis=1)
y = train_data_cleaned['SalePrice']

# Identify the categorical columns in X
categorical_columns = X.select_dtypes(include=['object']).columns

# Initialize a LabelEncoder for each categorical column
label_encoders = {column: LabelEncoder() for column in categorical_columns}

# Apply Label Encoding to each categorical column
for column in categorical_columns:
    X[column] = label_encoders[column].fit_transform(X[column])

# Display the first few rows of X to confirm the encoding
X.head()


# Split the first dataset (X, y) into train and test sets with a 70% - 30% split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.30, random_state=42)

# Fill NaN values in X_train and X_val with the median of the respective columns
X_train_filled = X_train.fillna(X_train.median())
X_val_filled = X_val.fillna(X_val.median())

(X_train.shape, X_val.shape, y_train.shape, y_val.shape)


# Create a Random Forest model
rf_model = RandomForestRegressor(random_state=42)

# Train the model on the training data
rf_model.fit(X_train_filled, y_train)

# Make predictions on the validation data
y_val_pred_filled = rf_model.predict(X_val_filled)

# Calculate the RMSE on the validation data
rmse_filled = sqrt(mean_squared_error(y_val, y_val_pred_filled))

# Print the RMSE
print(f'RMSE on the validation data: {rmse_filled}')

import time
from sklearn.metrics import mean_absolute_percentage_error

start_time = time.time()

# Define the parameter ranges
n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
max_features_range = ['sqrt', 'log2', None]  # None means using all features
max_depth_range = [1, 2, 5, 10, 20, None]  # None means no limit

# Initialize variables to store the best model and its RMSE and parameters
best_rmse = float('inf')
best_mape = float('inf')
best_model = None
best_parameters = {}

# Loop over all possible combinations of parameters
for n_estimators in n_estimators_range:
    for max_features in max_features_range:
        for max_depth in max_depth_range:
            # Create and train the Random Forest model
            rf_model = RandomForestRegressor(
                n_estimators=n_estimators,
                max_features=max_features,
                max_depth=max_depth,
                random_state=42
            )
            rf_model.fit(X_train_filled, y_train)
            
            # Make predictions and compute RMSE
            y_val_pred = rf_model.predict(X_val_filled)
            rmse = sqrt(mean_squared_error(y_val, y_val_pred))
            # Compute MAPE
            mape = mean_absolute_percentage_error(y_val, y_val_pred) * 100
            print(f"The parameters: {n_estimators}, {max_features}, {max_depth}. RMSE: {rmse}, MAPE: {mape}%")
            # If the model is better than the current best, update the best model and its parameters
            if rmse < best_rmse:
                best_rmse = rmse
                best_mape = mape
                best_model = rf_model
                best_parameters = {
                    'n_estimators': n_estimators,
                    'max_features': max_features,
                    'max_depth': max_depth
                }
print(f"The best parameters {best_parameters} for RMSE = {best_rmse}, MAPE: {mape}%")
end_time = time.time()
sequential_time = start_time - end_time
print(f"The sequential execution time is {end_time - start_time}")

# Initialize a lock to synchronize updates to best results
lock = Lock()

# Variables to store the best model and its parameters
best_rmse = float('inf')
best_mape = float('inf')
best_model = None
best_parameters = {}

# Function to evaluate a single set of parameters
def evaluate_params(n_estimators, max_features, max_depth):
    global best_rmse, best_mape, best_model, best_parameters

    # Create and train the Random Forest model
    rf_model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_features=max_features,
        max_depth=max_depth,
        random_state=42
    )
    rf_model.fit(X_train_filled, y_train)
    
    # Make predictions and compute RMSE
    y_val_pred = rf_model.predict(X_val_filled)
    rmse = sqrt(mean_squared_error(y_val, y_val_pred))

    # Compute MAPE
    mape = mean_absolute_percentage_error(y_val, y_val_pred) * 100

    # Use a lock to safely update the best results
    with lock:
        print(f"The parameters: {n_estimators}, {max_features}, {max_depth}. RMSE: {rmse}, MAPE: {mape}%")
        if rmse < best_rmse:
            best_rmse = rmse
            best_mape = mape
            best_model = rf_model
            best_parameters = {
                'n_estimators': n_estimators,
                'max_features': max_features,
                'max_depth': max_depth
            }

# Start timing
start_time = time.time()

# Define the parameter ranges
n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
max_features_range = ['sqrt', 'log2', None]  # None means using all features
max_depth_range = [1, 2, 5, 10, 20, None]  # None means no limit

# Create a list to hold the threads
threads = []

# Start a thread for each combination of parameters
for n_estimators in n_estimators_range:
    for max_features in max_features_range:
        for max_depth in max_depth_range:
            thread = Thread(target=evaluate_params, args=(n_estimators, max_features, max_depth))
            threads.append(thread)
            thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# End timing
end_time = time.time()
execution_time = end_time - start_time
print(f"The best parameters {best_parameters} for RMSE = {best_rmse}, MAPE: {best_mape}%")
print(f"The parallel execution time using Threading is {execution_time} seconds")
