from Healthcare.Configuration.mongo_db_connection import MongoDBClient
from Healthcare.exceptions import HealthCareException
import os,sys
from Healthcare.logger import logging
from Healthcare.Pipeline import training_pipeline
from Healthcare.Pipeline.training_pipeline import TrainPipeline
import os
from Healthcare.Utils.main_utils import read_yaml_file
from Healthcare.Constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI
from Healthcare.Constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from Healthcare.ML.model.estimator import ModelResolver,TargetValueMapping
from Healthcare.Utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
from Healthcare.Constant.training_pipeline import ARTIFACT_DIR,DATA_INGESTION_DIR_NAME,DATA_INGESTION_INGESTED_DIR,TARGET_COLUMN
import pandas as pd

env_file_path=os.path.join(os.getcwd(),"env.yaml")

def uvicorset_env_variable(env_file_path):

    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe
        test_df_path = os.path.join(ARTIFACT_DIR,max(os.listdir(ARTIFACT_DIR)),DATA_INGESTION_DIR_NAME,DATA_INGESTION_INGESTED_DIR,'test.csv')
        test_df = pd.read_csv(test_df_path)
        y_true = test_df[[TARGET_COLUMN]]
        test_df = test_df.drop([TARGET_COLUMN],axis=1)

        base_path = os.path.join(os.getcwd(),'artifact')
        latest_folder = max(os.listdir(os.path.join(os.getcwd(),'artifact')))
        latest_model_path = os.path.join(base_path,latest_folder,'model_trainer','trained_model')

        logging.info(f"Latest Model Path: {latest_model_path}")

        model_resolver = ModelResolver(model_dir=latest_model_path)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        # best_model_path = model_resolver.get_best_model_path()
        best_model_path = os.path.join(latest_model_path,"model.pkl")
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(test_df)
        test_df['predicted_column'] = y_pred
        test_df['y_true'] = y_true
        test_df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        test_df.to_csv(os.path.join(os.path.dirname(test_df_path),'predicted_test.csv'),index=False,header=True)
        
        logging.info("Prediction Done")
        return Response("Prediction Completed")
        
        #decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        # set_env_variable(env_file_path)
        training_pipeline = TrainPipeline()
        data_ingestion_artifact = training_pipeline.run_pipeline()
        
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    # main()
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)