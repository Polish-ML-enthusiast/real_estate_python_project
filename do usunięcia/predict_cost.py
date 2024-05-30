import joblib
from EDA import get_processed_data


# Reading the dataset from the get_processed_data function
data = get_processed_data()
 
def predict(data):
    lr = joblib.load('lr_model.sav')
    return lr.predict(data) 