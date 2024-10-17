# Climate Analysis API

This project is a Flask API that provides access to climate data for Honolulu, Hawaii. The API allows users to retrieve various climate-related information, including precipitation data, station information, temperature observations, and statistical summaries.

## Features

- **Precipitation Data**: Retrieve the last 12 months of precipitation data.
- **Station Information**: Get a list of weather stations.
- **Temperature Observations**: Query temperature observations for the most active station.
- **Statistical Analysis**: Calculate minimum, average, and maximum temperatures for specified date ranges.

## Installation

To use this API, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/criswait/sqlalchemy-challenge.git


## Usage
Access the API endpoints in your browser or API client:

Homepage: /
Precipitation Data: /api/v1.0/precipitation
Station Information: /api/v1.0/stations
Temperature Observations: /api/v1.0/tobs
Temperature Stats: /api/v1.0/<start> or /api/v1.0/<start>/<end>
