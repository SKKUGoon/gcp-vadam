# TODO: 
# 1. Clustering
# 2. Make it into a machine learning container


# Workflow
# 1. Data
# 2. Cleaning
# 3. Clustering - Hyperparameter tuning at the beginning
# 4. Initiate KNN to 

import pandas as pd
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from database.access import SDA
from datetime import datetime


class SeoulMovingCluster:
    def __init__(self):
        self.db = SDA()
    
    def get_data(self, start_date: datetime, end_date: datetime):
        # TODO: Get data from database
        data = ...

        # TODO: Clean data

        # Scale the data
        scaler = StandardScaler()
        
        data_scaled = scaler.fit_transform(data)
        data_scaled = pd.DataFrame(data_scaled, columns=data.columns)

        return data, data_scaled

    @staticmethod
    def tuning_dbscan(data: pd.DataFrame, min_samples: int):
        # Tuning EPSILON
        neighbors = NearestNeighbors(n_neighbors=min_samples)
        neighbors_fit = neighbors.fit(data)
        distances, indices = neighbors_fit.kneighbors(data)

        k_distances = np.sort(distances[:, min_samples - 1])
        
        diffs = np.diff(k_distances)  # Calculate the differences between consecutive points
        acceleration = np.diff(diffs)  # Calculate the rate of change (second derivative)
        elbow_idx = np.argmax(acceleration) + 1  # Find the point where acceleration is maximum (sharpest change)
        epsilon = k_distances[elbow_idx]  # Get the corresponding epsilon value
        
        return epsilon, min_samples
    

    def dbscan_clustering(data: pd.DataFrame, epsilon: float, min_samples: int):
        dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
        data_labels = dbscan.fit_predict(data)

        return data_labels

    
