import base64
import os
from io import BytesIO

import grpc
from concurrent import futures
from datetime import datetime
import pandas as pd
from protos import service_pb2
from protos import service_pb2_grpc
import time
from insights import CO2_emssion_pattern


class CO2AnalyticsService(service_pb2_grpc.CO2AnalyticsServiceServicer):

    def UploadCSV(self, request, context):
        print("Upload request is running")
        global csv_path, data
        timestamp = datetime.now().astimezone().strftime("%Y%m%d%H%M%S")
        csv_path = f"./csv_dataset" + ".csv"

        with open(csv_path, "wb") as f:
            f.write(request.file_content)

        try:
            data = pd.read_csv(csv_path)
            return service_pb2.UploadCSVResponse(
                status="success",
                message=f"CSV uploaded and saved to {csv_path}"
            )
        except Exception as e:
            print("Error:", e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.UploadCSVResponse(status="failed", message="error")


    def GetCSV(self, request, context):
        print("Received GetCSV request")
        return service_pb2.GetCSVResponse()

    def UpdateCSV(self, request, context):
        print("Received UpdateCSV request")
        return service_pb2.UpdateCSVResponse()

    def GetInsightsPlot(self, request, context):
        print("Received GetInsightsPlot request")
        global csv_path, data
        csv_path = fr".\csv_dataset.csv"
        print(csv_path)
        if os.path.exists(csv_path):
            print("path exists")
            data = pd.read_csv(csv_path)
        else:
            return {"error": "CSV not found on server. Please check the file name."}

        if csv_path is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("CSV path not set. Use UploadCsv before anything.")
            return service_pb2.GetInsightsResponse()

        if data.empty:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("No csv loaded. Use /set_csv/ before anything.")
            return service_pb2.GetInsightsResponse()

        chart_data = CO2_emssion_pattern(data, facility_name=request.facility_name)

        if chart_data is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("No data available for this facility.")
            return service_pb2.GetInsightsResponse()

        chart_data_proto = service_pb2.ChartData(
            labels=chart_data["labels"],
            predicted_values=chart_data["predicted_values"],
            actual_values=chart_data["actual_values"]
        )

        return service_pb2.GetInsightsResponse(
            chart_data = chart_data_proto
        )



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_CO2AnalyticsServiceServicer_to_server(CO2AnalyticsService(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting server on port 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)  # Keep server alive for 1 day
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop(0)

if __name__ == '__main__':
    serve()

