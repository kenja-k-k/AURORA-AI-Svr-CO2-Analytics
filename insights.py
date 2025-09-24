# IMPORTS: Bringing in the tools we need
# -------------------------------

import pandas as pd               # Tool for handling tabular data (spreadsheets, CSVs)
import numpy as np                # Tool for working with numbers
import matplotlib                 # Tool for plotting graphs
matplotlib.use('Agg')             # 'Agg' makes sure plots can be created even without a display screen (useful on servers)
import matplotlib.pyplot as plt   # Shortcut to make charts and graphs
from sklearn.linear_model import Ridge           # Machine Learning model: Ridge Regression (used to find patterns/relationships)
from sklearn.metrics import mean_squared_error   # Tool to measure how accurate the model’s predictions are
import argparse                   # Tool that lets us run the code from the command line with arguments

# -------------------------------------------------------------------------------------
# FUNCTION 1: CO2_emssion_pattern
# What it does: returns data for the CO2 emission pattern chart, the output is for the following items: date (days in the recent month), Co2 emitted in tonnes and capture efficiency in percentages
# Purpose: Show the relationship between CO2 emissions and capture efficiency in the last month

def CO2_emssion_pattern(data, facility_name, plot=False):
   filtered = data[data["facility_name"] == facility_name].dropna(          # STEP 1: Only keep rows belonging to the requested facility and drop rows with missing values
        subset=["co2_emitted_tonnes", "capture_efficiency_percent", "co2_captured_tonnes"]
    )
   if filtered.empty:                                                       # If there is no usable data, stop here
        print(f"No data found for facility: {facility_name}")
        return None, None
   filtered["date"] = pd.to_datetime(filtered["date"], errors="coerce")     # STEP 2: Convert the 'date' column into a proper date format
   latest_month = filtered["date"].dt.to_period("M").max()                  # STEP 3: Focus only on the most recent month’s data
   filtered = filtered[filtered["date"].dt.to_period("M") == latest_month]
   x = filtered[["co2_emitted_tonnes"]]                                     # STEP 4: Define inputs (X) and target (Y) for the model
   y = filtered["co2_captured_tonnes"]
   d = filtered["date"]
   model = Ridge()                                                          # STEP 5: Train a Ridge Regression model on this data
   model.fit(x, y)
   y_pred = model.predict(x)                                                # Model predicts efficiency given emissions

   chart_data = {                                                           # STEP 6: Package results into a dictionary for dashboards
       "labels": d.dt.strftime("%Y-%m-%d").tolist() , # returning dates as labels
       "actual_values": x["co2_emitted_tonnes"].tolist(), # actual amount emitted in tonnes
       "predicted_values": y_pred.tolist(), # percentage captured from the emitted amount
       "min_emissions": filtered["co2_emitted_tonnes"].min(),
       "max_emissions": filtered["co2_emitted_tonnes"].max(),
       "total_emissions": filtered["co2_emitted_tonnes"].sum(),
       "total_captured": filtered["co2_captured_tonnes"].sum(),
       "facility_name": facility_name,
   }
   return chart_data

# -------------------------------------------------------------------------------------
# FUNCTION 2: detect_efficiency_pattern
# What it does: returns data for the CO2 emission pattern chart, the output is for the following items: date (days in the recent month), actual percentage of CO2 capture and predicted percentage of CO2 capture based on the historical data for the period
# Purpose: Compare actual vs predicted efficiency and raise inefficiency alerts

def detect_efficiency_pattern(data, facility_name):
    filtered = data[data["facility_name"] == facility_name].dropna(         # STEP 1: Filter for the chosen facility and drop missing values
        subset=["co2_emitted_tonnes", "capture_efficiency_percent"]
    )
    if filtered.empty:
        print(f"No data found for facility: {facility_name}")
        return None, None
    filtered["date"] = pd.to_datetime(filtered["date"], errors="coerce")    # STEP 2: Clean up date column
    latest_month = filtered["date"].dt.to_period("M").max()                 # STEP 3: Focus on the latest month’s entries
    filtered = filtered[filtered["date"].dt.to_period("M") == latest_month]
    x = filtered[["co2_emitted_tonnes"]]                                    # STEP 4: Inputs (emissions) and target (efficiency)
    y = filtered["capture_efficiency_percent"]
    d = filtered["date"]
    model = Ridge()                                                         # STEP 5: Train Ridge Regression model and predict efficiency
    model.fit(x, y)
    y_pred = model.predict(x)
    inefficiency_flag = ((y_pred - y) / y_pred) > 0.05                      # STEP 6: Flag inefficiencies, If actual capture is more than 5% lower than predicted, raise a flag (True = problem)
    chart_data = {                                                          # STEP 7: Prepare dashboard-ready output
        "labels": d.dt.strftime("%Y-%m-%d").tolist(),  # returning dates as labels
        "actual_values": y.tolist(),  # actual percentage of CO2 capture
        "predicted_values": y_pred.tolist(),  # predicted percentage of CO2 capture
        "inefficiency_flag": inefficiency_flag.tolist() # alerts us if the actual capture value is more than 5% lower than the predicted
    }
    return chart_data

# -------------------------------------------------------------------------------------
# FUNCTION 3: storage_efficiency_pattern
# Purpose: Predict how much CO2 should have been stored and check if actual storage is lower
# What it does: analyses and finds the predicted amount of stored CO2 based on the historical data, it also provides an alert (a flag) when the CO2 level is lower than the predicted value

def storage_efficiency_pattern(data, facility_name):
    filtered = data[data["facility_name"] == facility_name].dropna(           # STEP 1: Filter out missing rows
        subset=["co2_emitted_tonnes", "co2_captured_tonnes", "co2_stored_tonnes"]
    )
    if filtered.empty:
        print(f"No data found for facility: {facility_name}")
        return None, None
    filtered["date"] = pd.to_datetime(filtered["date"], errors="coerce")      # STEP 2: Ensure 'date' is in proper datetime format
    latest_month = filtered["date"].dt.to_period("M").max()                   # STEP 3: Only keep latest month’s data
    filtered = filtered[filtered["date"].dt.to_period("M") == latest_month]
    x = filtered[["co2_emitted_tonnes", "co2_captured_tonnes"]]  # STEP 4: Features and target, we include both features in order to better predict co2_stored_tonnes, the model can see the effectiveness of capturing the release CO2
    y = filtered["co2_stored_tonnes"]
    d = filtered["date"]
    model = Ridge()                                              # STEP 5: Train regression model and make predictions
    model.fit(x, y)
    y_pred = model.predict(x) #predicted value of how much should be stored based on historical data
    storage_issue_flag = y < y_pred                              # STEP 6: Flag storage issues if actual < predicted

    dashboard_insights = {                                       # STEP 7: Package results for the dashboard
        "labels": d.dt.strftime("%Y-%m-%d").tolist(), # dates
        "actual_stored_co2": y.tolist(),
        "predicted_stored_co2": y_pred.tolist(),
        "storage_issue_detected": storage_issue_flag.tolist() # allows us to see on which days the storage level was lower than predicted
    }
    return dashboard_insights


#Run from cli______________________________
if __name__ == "__main__":
#section allows script to be run manually by user in the terminal:    
    parser = argparse.ArgumentParser(description="Get emission patterns per facility")
    parser.add_argument("csv_file", type=str, help="Path to the csv with emission data")
    parser.add_argument("--facility", type=str, help="Facility name", required=True)
    parser.add_argument("--plot", action="store_true", help="Plot L2 for analyrics")
    parser.add_argument("--scatter", action="store_true", help="Get the scatter plot along with L2")
    args = parser.parse_args()
    data = pd.read_csv(args.csv_file) # Load the CSV file into a pandas DataFrame
    CO2_emssion_pattern(data, args.facility, plot=args.plot, scatter=args.scatter) # Run one of the functions (basic CO2 pattern analysis)
    #_________________________________________________________
