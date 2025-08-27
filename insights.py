import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import argparse


#Main function for analytics. This may use different models_________
def CO2_emssion_pattern(data, facility_name, plot=False):
    filtered = data[data["facility_name"] == facility_name].dropna(
        subset=["co2_emitted_tonnes", "capture_efficiency_percent"]
    )

    if filtered.empty:
        print(f"No data found for facility: {facility_name}")
        return None, None

    x = filtered[["co2_emitted_tonnes"]]
    y = filtered["capture_efficiency_percent"]

    model = Ridge()
    model.fit(x, y)
    y_pred = model.predict(x)

    chart_data = {
        "labels": x["co2_emitted_tonnes"].astype(str).tolist(),  # X-axis
        "predicted_values": y_pred.tolist(),  # regression line
        "actual_values": y.tolist()  # actual measurements
    }
    return chart_data

#__________________________________________________________________

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