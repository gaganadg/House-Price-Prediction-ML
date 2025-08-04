import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# 1. Load the dataset
df = pd.read_csv("train.csv")

# 2. Select required columns
df = df[["LotArea", "BedroomAbvGr", "FullBath", "SalePrice"]]

# 3. Check for missing values
print("\nMissing values in each column:")
print(df.isnull().sum())

# 4. Split into Features (X) and Target (y)
X = df[["LotArea", "BedroomAbvGr", "FullBath"]]
y = df["SalePrice"]

# 5. Train-Test Split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)

# 6. Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

print("\nModel trained successfully!")

# 7. Make predictions
y_pred = model.predict(X_test)

# 8. Evaluate the model
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nR² Score:", r2)
print("Mean Absolute Error:", mae)
print("Root Mean Squared Error:", rmse)

# 9. Visualize Predictions
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Actual vs Predicted House Prices")
plt.savefig("house_price_predictions.png", dpi=300)  # Save the figure
plt.show()

import joblib

# Save the trained model
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")

