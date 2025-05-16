# Audio Recommendation System

## Overview

This project is a Python-based audio recommendation system designed to suggest similar audio content to users. It utilizes machine learning techniques, specifically Alternating Least Squares (ALS) and K-Nearest Neighbors (KNN), to provide personalized recommendations. The system fetches data from an API, processes it, trains recommendation models, and serves recommendations via a FastAPI web service.

## Features

* **Data Fetching:** Fetches audio interaction logs from a specified API, handling pagination.
* **Data Processing:** Cleans and transforms the fetched data into a suitable format for model training.
* **Model Training:** Trains ALS and KNN models on the processed data to capture user-audio interactions and audio similarity.
* **Recommendation Serving:** Provides an API endpoint using FastAPI to retrieve audio recommendations for a given audio ID.
* **Logging:** Includes a logging mechanism to track data fetching, processing, model training, and API usage.
* **Weekly Data Handling:** Processes data on a weekly basis, storing it in Parquet files with timestamps.
* **Model Persistence:** Saves trained models and mapping data for future use.
* **Error Handling:** Implements error handling for API requests, data processing, and model loading.

## Architecture

The system comprises the following components:

1.  **Data Fetching (`fetch_data.py`)**
    * Fetches data from the API.
    * Handles paginated responses.
    * Saves raw data to Parquet files.
    * Includes error handling and logging.

    ```python
    def fetch_paginated_data(base_url):
        # Function implementation
        pass
    ```

2.  **Data Processing & Model Training (`recommendation_als.ipynb`)**
    * Fetches data using `fetch_paginated_data`.
    * Processes the data with pandas.
    * Trains an ALS model using the `implicit` library.
    * Trains a KNN model using `scikit-learn`.
    * Saves the trained models and mapping files using `joblib`.
    * Implements weekly data processing and storage.

    ```python
    def fetch_and_save_weekly_data():
        # Function implementation
        pass
    ```

3.  **API Service (`main.py`)**
    * Uses FastAPI to create an API.
    * Loads the trained models.
    * Provides an endpoint to get audio recommendations.
    * Handles requests and returns recommendations.
    * Includes error handling.

    ```python
    @app.get("/recommendations/{audio_id}")
    async def get_recommendations(audio_id: int, top_n: int = 10):
        # Function implementation
        pass
    ```

4.  **Utilities (`utils.py`)**
    * Provides utility functions for logging and file management.

    ```python
    def log_message(message):
        # Function implementation
        pass

    def get_latest_file(folder, pattern, ext):
        # Function implementation
        pass
    ```

## Data Flow

1.  **Data Collection:** The `fetch_data.py` script fetches data from the API and saves it as Parquet files.  The  `recommendation_als.ipynb`  notebook orchestrates this.
2.  **Data Storage:** Data is stored in Parquet files, organized by week.
3.  **Model Training:** The  `recommendation_als.ipynb`  notebook reads the Parquet files, processes the data, and trains the ALS and KNN models.
4.  **Model Serving:** The `main.py` script loads the trained models and serves recommendations through a REST API.
5.  **Recommendations:** When a user requests recommendations for an audio ID, the API uses the loaded models to generate and return a list of recommended audio IDs.

