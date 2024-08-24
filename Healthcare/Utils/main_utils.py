
import yaml
from Healthcare.exceptions import HealthCareException
from Healthcare.logger import logging
import os,sys
import numpy as np
import dill
import pandas as pd
from typing import List

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HealthCareException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise HealthCareException(e, sys)



def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HealthCareException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HealthCareException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise HealthCareException(e, sys) from e


def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
      
        return obj
    except Exception as e:
        raise HealthCareException(e, sys) from e
    

def create_schema(dataframe:pd.DataFrame, drop_cols:List=[])->dict:

    """
    This function creates schema file of the input dataframe.
    Args: Input Dataframe
    Return: Dictionary
    """
    try:

        data_dict = {}
        col_list = []
        for col in dataframe.columns:
            if 'object' in str(dataframe[col].dtypes):col_list.append({col:'category'})
            elif 'int' in str(dataframe[col].dtypes):col_list.append({col:'int'})   
            else:col_list.append({col:'double'})
                

        numerical_col = [ col for col in dataframe.columns if 'int' in str(dataframe[col].dtype)]
        cat_col = [col for col in dataframe.columns if 'object' in str(dataframe[col].dtype)]


        data_dict.update({'columns':col_list})
        numerical_col_temp = []
        
        for col in numerical_col:
            numerical_col_temp.append({col:'int'})

        data_dict.update({'Numerical Column':numerical_col_temp})
        cat_col_temp = []

        for col in cat_col:
            cat_col_temp.append({col:'category'})

        data_dict.update({'cat_col':cat_col_temp})
        data_dict.update({'drop_col':drop_cols})

        return data_dict
    except Exception as e:
        raise HealthCareException(e,sys)

 