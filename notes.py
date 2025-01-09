
"""
Network Latency Tester Streamlit App

This script is a Streamlit application designed to test the network latency
of a specified URL by sending multiple HTTP requests using the `curl` command.
It collects various metrics such as DNS lookup time, TCP connect time, SSL
handshake time, server processing time, and total time. The results are displayed
in both tabular and graphical formats, with additional features for saving metrics
to a CSV file.

Key Features:
- Allows users to configure the test by specifying the URL, number of requests, 
  and delay between each request through the Streamlit sidebar.
- Displays a progress bar and real-time status updates for each request.
- Collects metrics for each request and converts them into milliseconds for better readability.
- Outputs the metrics in a DataFrame format and allows the user to download it as a CSV file.
- Visualizes the metrics using a bar chart with gridlines for easy interpretation.

Classes:
- NetworkLatencyTester:
    - Handles the HTTP requests, collects metrics, converts them to a DataFrame,
      and plots a bar chart.

Functions:
- main():
    - The entry point for the Streamlit application. Manages the user interface,
      handles input parameters, performs the latency test, and displays results.

Usage:
1. Enter the URL to test in the "URL to Test" field in the Streamlit sidebar.
2. Specify the number of requests and delay between each request.
3. Click the "Start Test" button to perform the test.
4. View the results in a DataFrame and a colorful bar chart.
5. Optionally download the metrics as a CSV file for further analysis.

Notes:
- Ensure that `curl` is installed and available in the system's PATH.
- The bar chart includes gridlines for better visualization.
- All metrics are displayed in milliseconds (ms) for uniformity.

Author: Mohan Chinnappan
"""