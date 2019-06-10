import pandas as pd
import requests
from lstm import createLaggedFrame, cleanUpDataframe, model_fit, df_preprocessing

LOOKBACK = 4
PREDICTION = 1

# request individual products to train. Not yet implemented in the database
# EXAMPLE: requests.get(f"http://localhost:8000/api/sales/{id}")
#response = requests.get("http://localhost:8000/api/sales")
#jsonObject = response.json()
#main_df = pd.DataFrame(jsonObject)
main_df = pd.read_csv("./weekly_data_with_features_and_weeknumbers.csv")
main_df = df_preprocessing(main_df)
new_df = createLaggedFrame(main_df, LOOKBACK, PREDICTION)
X_train_vals, X_valid_vals, Y_train, Y_valid = cleanUpDataframe(new_df, PREDICTION)
model_fit(X_train_vals, X_valid_vals, Y_train, Y_valid)