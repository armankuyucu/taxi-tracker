# Taxi Tracker App

## Overview

This Django-based project visualizes the historical locations of Swedish taxis on an interactive Google Map interface. The dataset used can be found [here](https://www.kaggle.com/datasets/henrikengdahl/taximovementconcatenated).

## Features

- **User Registration and Authentication**: Users can register, log in, and log out.
- **Data Storage**: Utilizes MongoDB for storing taxi location data and SQLite for user data.
- **Google Maps Integration**: Displays taxi locations on a Google Map.
- **Filtering**: Users can filter the taxi locations by time.
- **Custom Markers**: Different markers are used to represent two different taxis.

## Setup and Usage Instructions 

### Prerequisites

- Python 3.9
- Conda
- MongoDB
- Google Maps API Key

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/armankuyucu/taxi-tracker.git
   ```
2. Change the directory:
   ```bash
   cd taxi-tracker
   ```
3. Install the required packages:
   ```bash
   conda env create -f taxi_tracker.yml
   ```
4. Activate the conda environment:
   ```bash
    conda activate taxi-tracker
    ```
5. Make migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the application:
   ```bash
   python manage.py runserver
   ```
7. Open the app in your browser:
   ```http://127.0.0.1:8000/```


## Automated Tests
This application has unit tests, integration tests, and end-to-end tests. 22 tests are implemented in total.

To run the automated tests, execute the following command:
```bash
python manage.py test
```

## Screenshot

![image](https://github.com/user-attachments/assets/fe297f9a-6a7e-490a-89cd-d7df15d214f4)