from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

# Data structure to hold parsed CSV data
traffic_data = {
    "browsername": {},
    "platformname": {},
    "vertical": {},
    "country": {}
}


def ingest_data():
    """
    Method that reads the 4 csv files already given to us, and fill the traffic_data structure with the data from the csv's
    """
    csv_files = ["browsername.csv", "platformname.csv", "vertical.csv", "countries.csv"]
    for file_name in csv_files:
        with open(file_name, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            category = reader.fieldnames[0]  # Assuming the first column is the category
            for row in reader:
                traffic_data[category][row[category]] = float(row['opps'])


# Estimate traffic count based on provided criteria
def estimate_traffic(browser=None, platform=None, vertical=None, country=None, total_request_count=None):
    """
     Method that accepts four params from the request and calculated how many of the Total Request Count match the specified targeting criteria.
    @param browser: Browser (e.g., Chrome, Edge) - omitted when all browsers
    @param platform: Platform Name (e.g., Windows, Mac) - omitted when all platforms
    @param vertical: Vertical (e.g., Finance, Entertainment)  - omitted when all verticals
    @param country: Country (e.g. BG, US) - omitted when all countries
    @param total_request_count: Total Request Count (e.g. 100000000)
    @return: Calculated traffic as number
    """
    estimated_traffic = 0

    for category, filter_values in zip(["browsername", "platformname", "vertical", "country"],
                                       [browser, platform, vertical, country]):
        if filter_values is not None:
            for key, value in traffic_data[category].items():
                if any(filter_value.lower() in key.lower() for filter_value in filter_values):
                    estimated_traffic += value

    if total_request_count is not None:
        total_categories = sum(len(traffic_data[category]) for category in traffic_data)
        estimated_traffic = (estimated_traffic / total_categories) * total_request_count

    return int(estimated_traffic)


# API endpoint for traffic estimation
@app.route('/estimate_traffic', methods=['GET'])
def get_estimated_traffic():
    """
     Api endpoint "/estimate_traffic" which we sent to calculate the desire traffic

    """

    browser = request.args.getlist('browser')
    platform = request.args.getlist('platform')
    vertical = request.args.getlist('vertical')
    country = request.args.getlist('country')
    total_request_count = int(request.args.get('total_request_count', 0))

    estimated_traffic = estimate_traffic(browser, platform, vertical, country, total_request_count)

    return jsonify({"estimated_traffic": estimated_traffic})


# Documentation endpoint
@app.route('/', methods=['GET'])
def documentation():
    """
    Api endpoint that contains the documentation of how to use the api

    """
    return """
    <h1>Traffic Estimation API Documentation</h1>
    <p>Usage: /estimate_traffic</p>
    <p>Parameters:</p>
    <ul>
    <li>browser (optional, multivalued)</li>
    <li>platform (optional, multivalued)</li>
    <li>vertical (optional, multivalued)</li>
    <li>country (optional, multivalued)</li>
    <li>total_request_count (optional)</li>
    </ul>
    <p>Example: /estimate_traffic?browser=Chrome&platform=Windows&total_request_count=100000000</p>
    """


if __name__ == '__main__':
    ingest_data()
    app.run(debug=True)
