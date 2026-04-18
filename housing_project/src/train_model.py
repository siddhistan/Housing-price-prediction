import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 1. Load the cleaned data
df = pd.read_csv('housing_project/data/processed/cleaned_train.csv')

# 2. Setup Features and Target
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath']
X = df[features]
y = df['SalePrice']

# 3. THE REAL TEST: Split data into Train and Test sets
# We train on 80%, then test on 20% it has NEVER seen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training R^2: {train_score:.4f}")
print(f"Final Test R^2 (The Real Grade): {test_score:.4f}")

# 6. Save the model to your models folder
# Match the filename already in your folder
joblib.dump(model, 'housing_project/models/model_v1.pkl')

print("Model successfully overwritten in models/model_v1.pkl")