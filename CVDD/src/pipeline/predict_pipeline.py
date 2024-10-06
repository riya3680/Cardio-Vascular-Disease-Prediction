import sys
import pandas as pd
import dill
from src.exception import CustomException
#from src.utils import load_object
import dill


class predictpipeline:
    def __init__(self):
        pass
    def predict(self,features):
        try:
            model_path = 'model.pkl'
            model = load_object(file_path=model_path)
            preds = model.predict(features)
            return preds
        except:
            pass

           # raise CustomException(Exception, sys)


#map all the input data from html to backend
class customdata:
    def __init__(self, age, sex, cp, trestbps, chol, fbs, restecg, thalach,
       exang, oldpeak, slope, ca, thal):
        self.age = age
        self.sex = sex
        self.cp = cp
        self.trestbps = trestbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.slope = slope
        self.ca = ca
        self.thal = thal

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "age": [self.age],
                "sex": [self.sex],
                "cp": [self.cp],
                "trestbps": [self.trestbps],
                "chol": [self.chol],
                "fbs": [self.fbs],
                "restecg": [self.restecg],
                "thalach": [self.thalach],
                "exang": [self.exang],
                "oldpeak": [self.oldpeak],
                "slope": [self.slope],
                "ca": [self.ca],
                "thal": [self.thal]
            }
            print(f"The custom data : {custom_data_input_dict}")
            return pd.DataFrame(custom_data_input_dict)
        except:
            pass

            #raise CustomException(Exception, sys)




def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return dill.load(file_obj)
    except:
        pass

        #raise CustomException(Exception, sys)
