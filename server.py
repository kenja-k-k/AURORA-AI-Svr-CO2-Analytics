import grpc
from concurrent import futures
import time

from protos import service_pb2
from protos import service_pb2_grpc

# Implement the service by subclassing the generated Servicer class
class CO2AnalyticsService(service_pb2_grpc.CO2AnalyticsServiceServicer):

    def UploadCSV(self, request, context):
        # Your implementation here
        print("Received UploadCSV request")
        # Return a placeholder response (customize with actual response data)
        return service_pb2.UploadCSVResponse()

    def GetCSV(self, request, context):
        print("Received GetCSV request")
        return service_pb2.GetCSVResponse()

    def UpdateCSV(self, request, context):
        print("Received UpdateCSV request")
        return service_pb2.UpdateCSVResponse()

    def GetInsightsPlot(self, request, context):
        print("Received GetInsightsPlot request")
        return service_pb2.GetInsightsResponse()

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

