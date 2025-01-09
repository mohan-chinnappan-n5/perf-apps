import streamlit as st
import subprocess
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


class NetworkLatencyTester:
    def __init__(self, url, num_requests, delay):
        self.url = url
        self.num_requests = num_requests
        self.delay = delay
        self.metrics = {
            "DNS Lookup Time (ms)": [],
            "TCP Connect Time (ms)": [],
            "SSL Handshake Time (ms)": [],
            "Server Processing Time (ms)": [],
            "Total Time (ms)": [],
        }

    def perform_requests(self, progress_bar, status_text):
        """Perform the requests and collect metrics."""
        for i in range(self.num_requests):
            # Update the progress bar and status
            progress_bar.progress((i + 1) / self.num_requests)
            status_text.text(f"Performing request #{i + 1}...")

            # Run the curl command
            result = subprocess.run(
                [
                    "curl",
                    "-o", "/dev/null",
                    "-s",
                    "-w",
                    "DNS Lookup Time: %{time_namelookup}\n"
                    "TCP Connect Time: %{time_connect}\n"
                    "SSL Handshake Time: %{time_appconnect}\n"
                    "Server Processing Time: %{time_starttransfer}\n"
                    "Total Time: %{time_total}\n",
                    self.url,
                ],
                capture_output=True,
                text=True,
            )

            # Parse the metrics and convert to milliseconds
            for line in result.stdout.splitlines():
                metric, value = line.split(": ")
                metric_ms = metric + " (ms)"  # Update metric name for milliseconds
                self.metrics[metric_ms].append(float(value) * 1000)  # Convert to ms

            # Wait for the specified delay before the next request
            if i < self.num_requests - 1:
                time.sleep(self.delay)

        # Clear the progress bar and status text when done
        progress_bar.empty()
        status_text.text("Requests completed!")

    def to_dataframe(self):
        """Convert metrics to a Pandas DataFrame."""
        data = {metric: self.metrics[metric] for metric in self.metrics}
        data["Request Number"] = [i + 1 for i in range(len(self.metrics["DNS Lookup Time (ms)"]))]
        return pd.DataFrame(data)

    def plot_metrics(self):
        """Plot the metrics as a bar chart."""
        num_metrics = len(self.metrics)
        x = np.arange(len(self.metrics["DNS Lookup Time (ms)"]))  # Number of requests
        width = 0.15  # Bar width

        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot each metric as a separate bar
        for i, (metric, values) in enumerate(self.metrics.items()):
            ax.bar(x + i * width, values, width, label=metric)

        # Add labels, legend, and title
        ax.set_xlabel("Request Number")
        ax.set_ylabel("Time (ms)")
        ax.set_title("Request Timing Metrics (in ms)")
        ax.set_xticks(x + (num_metrics - 1) * width / 2)
        ax.set_xticklabels([f"#{i + 1}" for i in range(len(self.metrics["DNS Lookup Time (ms)"]))])
        ax.legend()

        # Add grid for better readability
        ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

        plt.tight_layout()
        return fig


# Streamlit App
def main():
    st.title("Network Latency Tester (in ms)")
    st.sidebar.header("Test Configuration")

    # Sidebar inputs
    url = st.sidebar.text_input("URL to Test", value="https://api.example.com/endpoint")
    num_requests = st.sidebar.number_input("Number of Requests", min_value=1, value=5, step=1)
    delay = st.sidebar.number_input("Delay Between Requests (seconds)", min_value=0.1, value=1.0, step=0.1)

    # Start test button
    if st.sidebar.button("Start Test"):
        tester = NetworkLatencyTester(url, num_requests, delay)

        # Add progress bar and status text
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Perform requests
        tester.perform_requests(progress_bar, status_text)

        # Display metrics as a DataFrame
        df = tester.to_dataframe()
        st.subheader("Request Metrics (in ms)")
        st.dataframe(df)

        # Save CSV file
        csv_file = "metrics.csv"
        df.to_csv(csv_file, index=False)
        st.success(f"Metrics saved to {csv_file}")
        st.download_button("Download CSV", df.to_csv(index=False), file_name=csv_file, mime="text/csv")

        # Plot the metrics
        st.subheader("Metrics Chart (in ms)")
        fig = tester.plot_metrics()
        st.pyplot(fig)


if __name__ == "__main__":
    main()