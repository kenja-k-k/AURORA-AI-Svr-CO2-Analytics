<h1>On demand CO2 analytics</h1>
This project is a fastapi based service for managing and analyzing CO2 emission data. 
It allows users to upload a CSV dataset, update with entries, and generate analytical insights with a model (currently L2), 
including an optional plot.

<h2>Usage</h2>
Use the requirements.txt to install all the necessary dependencies
The main entry point for the app is server.py which is gRPC server file with endpoints.
The app can be run in Docker by runing: 
```docker-compose build --no-cache``` to build the docker image 
then ```docker-compose up -d``` it will start the container.

The endpoints will be available at ```lochalhost:50051```

In order to test the service in Postman, you need to make sure to choose gRPC instead of HTTP. Postman requires .proto definition files
for methods and messages. Upload the file ```protos/service.proto``` that is available in the repo. This will allow Postman to identify endpoints 
that are used.
Example: ```localhost:50051/UploadCSV```

<h2>Endpoints</h2>
There are two main endpoints that are currently exposed and are ready for use:
<ul>
  <li><b> UploadCSV </b> This endpoint accepts a CSV file in base64 format as a string.
     ```localhost:50051/UploadCSV```
    ```{ "file_content": "base64 string here" }```
  </li>
    
  <li><b>GetInsightsPlot </b>This endpoint performs an L2 on the loaded data for a specific facility. 
    It returns a chart data points that can be used to construct a plot / graph showing the relationship between emissions and capture efficiency
    Example endpoint: ```localhost:50051/GetInsightsPlot
    Example input facility name: ```{ "facility_name": "Facility Name Here" }```

   <b>The process behind GetInsightsPlot</b>
   This process trains a regression model on the provided data, makes predictions, and prepares the results for visualization. The model is trained using the features extracted from the dataset file,
   after the training the model predicts the target values based on the input features giving us the values to see how effective CO2 capture was in relation to the emitted amount. Finally, it outputs the chart data
   that can be used for visualization and extracting useful insights about the facility (CCS plant)
    .</li>
</ul>

