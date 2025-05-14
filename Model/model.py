import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the dataset using pandas
dataset_path = os.path.join(current_dir, '../Data/District_Statewise_Well.csv')
if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path)
else:
    raise FileNotFoundError(f"File '{dataset_path}' not found.")

df = df.dropna()

# Extract features and target variables
X_resource = df[['Recharge from rainfall During Monsoon Season',
                 'Recharge from other sources During Monsoon Season',
                 'Recharge from rainfall During Non Monsoon Season',
                 'Recharge from other sources During Non Monsoon Season',
                 'Total Natural Discharges']]
y_resource = df['Annual Extractable Ground Water Resource']

# Split the data into training and testing sets
X_train_resource, X_test_resource, y_train_resource, y_test_resource = train_test_split(X_resource, y_resource, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor model
rf_resource = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf_resource.fit(X_train_resource, y_train_resource)


# Make predictions
predictions_resource = rf_resource.predict(X_test_resource)

# Evaluate the model
mse_resource = mean_squared_error(y_test_resource, predictions_resource)
r2_score_resource = r2_score(y_test_resource, predictions_resource)

print(f'Mean Squared Error for Annual Extractable Ground Water Resource: {mse_resource}')
print(f'R-squared Score for Annual Extractable Ground Water Resource: {r2_score_resource}')

# Split the entire dataset into training and testing sets
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# Save the training and testing datasets to CSV files
df_train.to_csv(os.path.join(current_dir, 'train_data.csv'), index=False)
df_test.to_csv(os.path.join(current_dir, 'test_data.csv'), index=False)
