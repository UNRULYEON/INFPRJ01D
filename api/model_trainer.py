import pandas as pd
import requests
from lstm import createLaggedFrame, cleanUpDataframe, model_fit

LOOKBACK = 7
PREDICTION = 1
PRODUCT_IDS = [1]

for id in PRODUCT_IDS:
    # request individual products to train. Not yet implemented in the database
    # EXAMPLE: requests.get(f"http://localhost:8000/api/sales/{id}")
    response = requests.get("http://localhost:8000/api/sales")
    jsonObject = response.json()
    main_df = pd.DataFrame(jsonObject)
    main_df = main_df.drop('date', axis=1)
    main_df = main_df.drop('id', axis=1)
    new_df = createLaggedFrame(main_df, LOOKBACK, PREDICTION)
    X_train_vals, X_valid_vals, Y_train, Y_valid = cleanUpDataframe(new_df, PREDICTION)
    model = model_fit(X_train_vals, X_valid_vals, Y_train, Y_valid, id)
