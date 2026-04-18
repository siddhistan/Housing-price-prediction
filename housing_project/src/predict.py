import joblib
import pandas as pd
import warnings
import sys  # <--- NEW: Necessary for the exit command

# 1. Setup & Load
warnings.filterwarnings("ignore", category=UserWarning)

# Path to the model you saved earlier
model_path = 'housing_project/models/model_v1.pkl'
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath']

try:
    model = joblib.load(model_path)
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}")
    sys.exit()

def get_input(label, range_text, min_v, max_v):
    """Prints the guide first, then asks for input with an exit option."""
    print(f"\n> {label}")
    print(f"  Range: {range_text} (or type 'q' to quit)")
    
    while True:
        user_choice = input("  Enter value: ").strip().lower()
        
        # Check for the Escape Hatch
        if user_choice in ['q', 'quit']:
            print("\nExiting Predictor... Have a great day!")
            sys.exit()
            
        try:
            val = float(user_choice)
            if min_v <= val <= max_v:
                return val
            print(f"  ! Please stay within {min_v} and {max_v}.")
        except ValueError:
            print("  ! Please enter a number or 'q' to quit.")

def main():
    print("========================================")
    print("   AI HOUSE PRICE APPRAISAL TOOL        ")
    print("========================================")
    print("Follow the prompts below to value a property.")

    # Guided Inputs using our robust helper function
    q_qual = get_input("Overall Quality", "[1: Poor] to [10: Luxury]", 1, 10)
    q_area = get_input("Living Area", "300 to 10,000 sq ft", 300, 10000)
    q_cars = get_input("Garage Size", "0 to 5 cars", 0, 5)
    q_bsmt = get_input("Basement Size", "0 to 5,000 sq ft", 0, 5000)
    q_bath = get_input("Full Bathrooms", "1 to 5 baths", 1, 5)

    # 2. Predict using a DataFrame
    user_data = pd.DataFrame([[q_qual, q_area, q_cars, q_bsmt, q_bath]], columns=features)
    price = model.predict(user_data)[0]

    print("\n" + "="*40)
    print(f" ESTIMATED VALUE: ${price:,.2f}")
    print("="*40)
    print("Appraisal complete.")

if __name__ == "__main__":
    main()