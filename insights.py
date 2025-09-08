import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import argparse

'''
This function returns data for the CO2 emission pattern chart, the output is for the following items: date (days in the recent month, Co2 emitted in tonnes
and capture efficiency in percentages
'''

def CO2_emssion_pattern(data, facility_name, plot=False):
   filtered = data[data["facility_name"] == facility_name].dropna(
        subset=["co2_emitted_tonnes", "capture_efficiency_percent"]
    )
   if filtered.empty:
        print(f"No data found for facility: {facility_name}")
        return None, None
   filtered["date"] = pd.to_datetime(filtered["date"], errors="coerce")
   latest_month = filtered["date"].dt.to_period("M").max()
   filtered = filtered[filtered["date"].dt.to_period("M") == latest_month]
   x = filtered[["co2_emitted_tonnes"]]
   y = filtered["capture_efficiency_percent"]
   d = filtered["date"]
   model = Ridge()
   model.fit(x, y)
   y_pred = model.predict(x)

   chart_data = {
       "labels": d.dt.strftime("%Y-%m-%d").tolist() , # returning dates as labels
       "actual_values": x["co2_emitted_tonnes"].tolist(), # actual amount emitted in tonnes
       "predicted_values": y.tolist(), # percentage captured from the emitted amount
   }
   return chart_data

'''
This function returns data for the CO2 emission pattern chart, the output is for the following items: date (days in the recent month, actual percentage of
CO2 capture amd predicted percentage of CO2 capture based on the historical data for the period
'''
def detect_efficiency_pattern(data, facility_name):
    filtered = data[data["facility_name"] == facility_name].dropna(
        subset=["co2_emitted_tonnes", "capture_efficiency_percent"]
    )
    if filtered.empty:
        print(f"No data found for facility: {facility_name}")
        return None, None
    filtered["date"] = pd.to_datetime(filtered["date"], errors="coerce")
    latest_month = filtered["date"].dt.to_period("M").max()
    filtered = filtered[filtered["date"].dt.to_period("M") == latest_month]
    x = filtered[["co2_emitted_tonnes"]]
    y = filtered["capture_efficiency_percent"]
    d = filtered["date"]
    model = Ridge()
    model.fit(x, y)
    y_pred = model.predict(x)
    inefficiency_flag = ((y_pred - y) / y_pred) > 0.05
    chart_data = {
        "labels": d.dt.strftime("%Y-%m-%d").tolist(),  # returning dates as labels
        "actual_values": y.tolist(),  # actual percentage of CO2 capture
        "predicted_values": y_pred.tolist(),  # predicted percentage of CO2 capture
        "inefficiency_flag": inefficiency_flag.tolist() # alerts us if the actual capture value is more than 5% lower than the predicted
    }
    return chart_data
#__________________________________________________________________

'''
This function analyses and finds the predicted amount of stored CO2 based on the historical data, it also provides an alert (a flag) when the CO2 level 
is lower the predicted value
'''
def storage_efficiency_pattern(data, facility_name):
    filtered = data[data["facility_name"] == facility_name].dropna(
        subset=["co2_emitted_tonnes", "co2_captured_tonnes", "co2_stored_tonnes"]
    )
    if filtered.empty:
        print(f"No data found for facility: {facility_name}")
        return None, None
    filtered["date"] = pd.to_datetime(filtered["date"], errors="coerce")
    latest_month = filtered["date"].dt.to_period("M").max()
    filtered = filtered[filtered["date"].dt.to_period("M") == latest_month]
    x = filtered[["co2_emitted_tonnes", "co2_captured_tonnes"]]  # we include both features in order to better predict co2_stored_tonnes, the model can see the effectiveness of capturing the release CO2
    y = filtered["co2_stored_tonnes"]
    d = filtered["date"]
    model = Ridge()
    model.fit(x, y)
    y_pred = model.predict(x) #predicted value of how much should be stored based on historical data
    storage_issue_flag = y < y_pred

    dashboard_insights = {
        "labels": d.dt.strftime("%Y-%m-%d").tolist(), # dates
        "actual_stored_co2": y.tolist(),
        "predicted_stored_co2": y_pred.tolist(),
        "storage_issue_detected": storage_issue_flag.tolist() # allows us to see on which days the storage level was lower than predicted
    }
    return dashboard_insights


#Run from cli______________________________
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Get emission patterns per facility")
    parser.add_argument("csv_file", type=str, help="Path to the csv with emission data")
    parser.add_argument("--facility", type=str, help="Facility name", required=True)
    parser.add_argument("--plot", action="store_true", help="Plot L2 for analyrics")
    parser.add_argument("--scatter", action="store_true", help="Get the scatter plot along with L2")
    args = parser.parse_args()
    data = pd.read_csv(args.csv_file)
    CO2_emssion_pattern(data, args.facility, plot=args.plot, scatter=args.scatter)
    #_________________________________________________________