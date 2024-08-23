import sys

import numpy as np
import pandas as pd
from typing import List
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import TargetEncoder

from Healthcare.Constant.training_pipeline import TARGET_COLUMN
from Healthcare.Entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from Healthcare.Entity.config_entity import DataTransformationConfig
from Healthcare.exceptions import HealthCareException
from Healthcare.logger import logging
from Healthcare.ML.model.estimator import TargetValueMapping
from Healthcare.Utils.main_utils import save_numpy_array_data, save_object




class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact, 
                    data_transformation_config: DataTransformationConfig,):
        """

        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise HealthCareException(e, sys)


    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise HealthCareException(e, sys)


    @classmethod
    def get_data_transformer_object(cls,num_col,cat_col,low_car_col,high_car_col)->Pipeline:
        try:
            logging.info(f"Colunm Transformer object Instantiated")
            ct = ColumnTransformer(
                [
                    ('Low Car',OneHotEncoder(handle_unknown='ignore',sparse_output=False),low_car_col),
                    ('High Car', TargetEncoder(target_type="multiclass"),high_car_col),
                    ("standardizer",RobustScaler(),num_col)
                ]
            )

            logging.info(f"Pipeline Object instantiated")
            preprocessor = Pipeline([
                ("column transformer",ct)
            ])
            
            return preprocessor

        except Exception as e:
            raise HealthCareException(e, sys) from e
        
    @staticmethod
    def get_numerical_and_cardinal_cols(x_train:pd.DataFrame)->List:

        logging.info("Getting Num & Cat col with Cardinality")
        try:
            cat_col = [col for col in x_train.columns if x_train[col].dtypes == 'object']
            num_col = [col for col in x_train.columns if x_train[col].dtypes != 'object']

            low_car_cat = []
            high_car_cat = []
            for col in cat_col:
                nunique = x_train[col].nunique()
                if nunique < 20:
                    low_car_cat.append(col)
                else:
                    high_car_cat.append(col)
            logging.info(f"Num Col: {num_col} Cat Col:{cat_col} low_cardinal_categorical: {low_car_cat} high_cardinal_categorical: {high_car_cat}")
            return num_col,cat_col,low_car_cat,high_car_cat
        except Exception as e:
            raise HealthCareException(e,sys)

    
    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        try:
            
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace( TargetValueMapping().to_dict())

            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())


            num_col,cat_col,low_car_col,high_car_col = self.get_numerical_and_cardinal_cols(input_feature_train_df)
            preprocessor = self.get_data_transformer_object(num_col,cat_col,low_car_col,high_car_col)


        
            preprocessor_object = preprocessor.fit(input_feature_train_df,target_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature =preprocessor_object.transform(input_feature_test_df)


            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df) ]

            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)
            
            
            #preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise HealthCareException(e, sys) from e
