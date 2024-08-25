# Healthcare-Prediction-System
The Health Prediction system is an end user support and online consultation project. Here we propose a system that allows users to get instant guidance on their health issues through an intelligent health care system online. The system is fed with various symptoms and the disease/illness associated with those systems. The system allows user to share their symptoms and issues. It then processes users symptoms to check for various illness that could be associated with 


## Run the Application
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. Also make sure the csv file in the data folder in loaded in the remote MONGODB database.

### Step 1-: Clone the Repository
```
git clone https://github.com/zama-sarib/Healthcare-Prediction-System.git
```

### Step 2-: Create conda environment
```
conda create -p ./env python=3.11 -y
```

### Step 3-: Activate Conda environment
```
conda activate ./env
```

### Step 4-: Install requirements
```
pip install -r requirements.txt
```

### Step 5-: Creating MongoDB Database and Collection
```
Create a MongoDB database = Healthcare and collection = healthcare
```
Note: Please take care of case of MongoDB database and collection name 


### Step 6-: Export the environment variable
```
export MONGODB_URL_KEY=<MONGODB_URL_KEY>

```

### Step 7-: Run the application server
```
python main.py
```

## Run Locally

### Build the Docker Image
```
docker build -t healthcare .
```

### Run the Docker Image

```
docker run -it -p 80:8080 -e MONGODB_URL_KEY=<MONGODB_URL_KEY> <IMAGEID OR IMAGENAME>
```
## Deployment to Azure

### Services used
- GitHub Actions for CI/CD
