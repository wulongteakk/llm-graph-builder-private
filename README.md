
# Knowledge Graph Builder App

Creating knowledge graphs from unstructured data


# LLM Graph Builder

![Python](https://img.shields.io/badge/Python-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-green)
![React](https://img.shields.io/badge/React-blue)

## Overview
This application is designed to turn Unstructured data (pdfs,docs,txt,youtube video,web pages,etc.) into a knowledge graph stored in Neo4j. It utilizes the power of Large language models (OpenAI,Gemini,etc.) to extract nodes, relationships and their properties from the text and create a structured knowledge graph using Langchain framework. 

Upload your files from local machine, GCS or S3 bucket or from web sources, choose your LLM model and generate knowledge graph.

## Key Features
- **Knowledge Graph Creation**: Transform unstructured data into structured knowledge graphs using LLMs.
- **Providing Schema**: Provide your own custom schema or use existing schema in settings to generate graph.
- **View Graph**: View graph for a particular source or multiple sources at a time in Bloom.
- **Chat with Data**: Interact with your data in a Neo4j database through conversational queries, also retrive metadata about the source of response to your queries. 

## Getting started

:warning: You will need to have a Neo4j Database V5.15 or later with [APOC installed](https://neo4j.com/docs/apoc/current/installation/) to use this Knowledge Graph Builder.
You can use any [Neo4j Aura database](https://neo4j.com/aura/) (including the free database)
If you are using Neo4j Desktop, you will not be able to use the docker-compose but will have to follow the [separate deployment of backend and frontend section](#running-backend-and-frontend-separately-dev-environment). :warning:


### 本地部署

[中文版（chinese version)](./README_ZH.md)

## Deployment
### Local deployment
#### Running through docker-compose
By default only OpenAI and Diffbot are enabled since Gemini requires extra GCP configurations.

In your root folder, create a .env file with your OPENAI and DIFFBOT keys (if you want to use both):
```env
OPENAI_API_KEY="your-openai-key"
DIFFBOT_API_KEY="your-diffbot-key"
```

if you only want OpenAI:
```env
LLM_MODELS="diffbot,openai-gpt-3.5,openai-gpt-4o"
OPENAI_API_KEY="your-openai-key"
```

if you only want Diffbot:
```env
LLM_MODELS="diffbot"
DIFFBOT_API_KEY="your-diffbot-key"
```

You can then run Docker Compose to build and start all components:
```bash
docker-compose up --build
```

#### Additional configs

By default, the input sources will be: Local files, Youtube, Wikipedia ,AWS S3 and Webpages. As this default config is applied:
```env
REACT_APP_SOURCES="local,youtube,wiki,s3,web"
```

If however you want the Google GCS integration, add `gcs` and your Google client ID:
```env
REACT_APP_SOURCES="local,youtube,wiki,s3,gcs,web"
GOOGLE_CLIENT_ID="xxxx"
```

You can of course combine all (local, youtube, wikipedia, s3 and gcs) or remove any you don't want/need.

### Chat Modes

By default,all of the chat modes will be available: vector, graph+vector and graph.
If none of the mode is mentioned in the chat modes variable all modes will be available:
```env
CHAT_MODES=""
```

If however you want to specify the only vector mode or only graph mode you can do that by specifying the mode in the env:
```env
CHAT_MODES="vector,graph+vector"
```

#### Running Backend and Frontend separately (dev environment)
Alternatively, you can run the backend and frontend separately:

- For the frontend:
1. Create the frontend/.env file by copy/pasting the frontend/example.env.
2. Change values as needed
   3.
    ```bash
    cd frontend
    yarn
    yarn run dev
    ```

- For the backend:
1. Create the backend/.env file by copy/pasting the backend/example.env.
2. Change values as needed
   3.
    ```bash
    cd backend
    python -m venv envName
    source envName/bin/activate 
    pip install -r requirements.txt
    uvicorn score:app --reload
    ```
### Deploy in Cloud
To deploy the app and packages on Google Cloud Platform, run the following command on google cloud run:
```bash
# Frontend deploy 
gcloud run deploy 
source location current directory > Frontend
region : 32 [us-central 1]
Allow unauthenticated request : Yes
```
```bash
# Backend deploy 
gcloud run deploy --set-env-vars "OPENAI_API_KEY = " --set-env-vars "DIFFBOT_API_KEY = " --set-env-vars "NEO4J_URI = " --set-env-vars "NEO4J_PASSWORD = " --set-env-vars "NEO4J_USERNAME = "
source location current directory > Backend
region : 32 [us-central 1]
Allow unauthenticated request : Yes
```

## ENV
| Env Variable Name       | Mandatory/Optional | Default Value | Description                                                                                      |
|-------------------------|--------------------|---------------|--------------------------------------------------------------------------------------------------|
| OPENAI_API_KEY          | Mandatory          |               | API key for OpenAI                                                                               |
| DIFFBOT_API_KEY         | Mandatory          |               | API key for Diffbot                                                                              |
| EMBEDDING_MODEL         | Optional           | all-MiniLM-L6-v2 | Model for generating the text embedding (all-MiniLM-L6-v2 , openai , vertexai)                |
| IS_EMBEDDING            | Optional           | true          | Flag to enable text embedding                                                                    |
| KNN_MIN_SCORE           | Optional           | 0.94          | Minimum score for KNN algorithm                                                                  |
| GEMINI_ENABLED          | Optional           | False         | Flag to enable Gemini                                                                             |
| GCP_LOG_METRICS_ENABLED | Optional           | False         | Flag to enable Google Cloud logs                                                                 |
| NUMBER_OF_CHUNKS_TO_COMBINE | Optional        | 5             | Number of chunks to combine when processing embeddings                                           |
| UPDATE_GRAPH_CHUNKS_PROCESSED | Optional      | 20            | Number of chunks processed before updating progress                                        |
| NEO4J_URI               | Optional           | neo4j://database:7687 | URI for Neo4j database                                                                  |
| NEO4J_USERNAME          | Optional           | neo4j         | Username for Neo4j database                                                                       |
| NEO4J_PASSWORD          | Optional           | password      | Password for Neo4j database                                                                       |
| LANGCHAIN_API_KEY       | Optional           |               | API key for Langchain                                                                             |
| LANGCHAIN_PROJECT       | Optional           |               | Project for Langchain                                                                             |
| LANGCHAIN_TRACING_V2    | Optional           | true          | Flag to enable Langchain tracing                                                                  |
| LANGCHAIN_ENDPOINT      | Optional           | https://api.smith.langchain.com | Endpoint for Langchain API                                                            |
| BACKEND_API_URL         | Optional           | http://localhost:8000 | URL for backend API                                                                       |
| BLOOM_URL               | Optional           | https://workspace-preview.neo4j.io/workspace/explore?connectURL={CONNECT_URL}&search=Show+me+a+graph&featureGenAISuggestions=true&featureGenAISuggestionsInternal=true | URL for Bloom visualization |
| REACT_APP_SOURCES       | Optional           | local,youtube,wiki,s3 | List of input sources that will be available                                               |
| LLM_MODELS              | Optional           | diffbot,openai-gpt-3.5,openai-gpt-4o | Models available for selection on the frontend, used for entities extraction and Q&A
| CHAT_MODES              | Optional           | vector,graph+vector,graph | Chat modes available for Q&A
| ENV                     | Optional           | DEV           | Environment variable for the app                                                                 |
| TIME_PER_CHUNK          | Optional           | 4             | Time per chunk for processing                                                                    |
| CHUNK_SIZE              | Optional           | 5242880       | Size of each chunk of file for upload                                                                |
| GOOGLE_CLIENT_ID        | Optional           |               | Client ID for Google authentication                                                              |
| GCS_FILE_CACHE        | Optional           | False              | If set to True, will save the files to process into GCS. If set to False, will save the files locally   |
| ENTITY_EMBEDDING        | Optional           | False              | If set to True, It will add embeddings for each entity in database |
| LLM_MODEL_CONFIG_ollama_<model_name>        | Optional           |               | Set ollama config as - model_name,model_local_url for local deployments |




###
To deploy the app and packages on Google Cloud Platform, run the following command on google cloud run:
```bash
# Frontend deploy 
gcloud run deploy 
source location current directory > Frontend
region : 32 [us-central 1]
Allow unauthenticated request : Yes
```
```bash
# Backend deploy 
gcloud run deploy --set-env-vars "OPENAI_API_KEY = " --set-env-vars "DIFFBOT_API_KEY = " --set-env-vars "NEO4J_URI = " --set-env-vars "NEO4J_PASSWORD = " --set-env-vars "NEO4J_USERNAME = "
source location current directory > Backend
region : 32 [us-central 1]
Allow unauthenticated request : Yes
```
### Features
- **PDF Upload**: Users can upload PDF documents using the Drop Zone.
- **S3 Bucket Integration**: Users can also specify PDF documents stored in an S3 bucket for processing.
- **Knowledge Graph Generation**: The application employs OpenAI/Diffbot's LLM to extract relevant information from the PDFs and construct a knowledge graph.
- **Neo4j Integration**: The extracted nodes and relationships are stored in a Neo4j database for easy visualization and querying.
- **Grid View of source node files with** : Name,Type,Size,Nodes,Relations,Duration,Status,Source,Model
  
## Functions/Modules

#### extract_graph_from_file(uri, userName, password, file_path, model):
   Extracts nodes , relationships and properties from a PDF file leveraging LLM models.

    Args:
     uri: URI of the graph to extract
     userName: Username to use for graph creation ( if None will use username from config file )
     password: Password to use for graph creation ( if None will use password from config file )
     file: File object containing the PDF file path to be used
     model: Type of model to use ('Gemini Pro' or 'Diffbot')
       
     Returns: 
     Json response to API with fileName, nodeCount, relationshipCount, processingTime, 
     status and model as attributes.

<img width="692" alt="neoooo" src="https://github.com/neo4j-labs/llm-graph-builder/assets/118245454/01e731df-b565-4f4f-b577-c47e39dd1748">

#### create_source_node_graph(uri, userName, password, file):

   Creates a source node in Neo4jGraph and sets properties.

    Args:
     uri: URI of Graph Service to connect to
     userName: Username to connect to Graph Service with ( default : None )
     password: Password to connect to Graph Service with ( default : None )
     file: File object with information about file to be added
       
    Returns: 
     Success or Failure message of node creation

<img width="958" alt="neo_workspace" src="https://github.com/neo4j-labs/llm-graph-builder/assets/118245454/f2eb11cd-718c-453e-bec9-11410ec6e45d">


#### get_source_list_from_graph():

     Returns a list of file sources in the database by querying the graph and 
     sorting the list by the last updated date. 

<img width="822" alt="get_source" src="https://github.com/neo4j-labs/llm-graph-builder/assets/118245454/1d8c7a86-6f10-4916-a4c1-8fdd9f312bcc">

#### Chunk nodes and embeddings creation in Neo4j

<img width="926" alt="chunking" src="https://github.com/neo4j-labs/llm-graph-builder/assets/118245454/4d61479c-e5e9-415e-954e-3edf6a773e72">


## Application Walkthrough
https://github.com/neo4j-labs/llm-graph-builder/assets/121786590/b725a503-6ade-46d2-9e70-61d57443c311


## Usage
1. Connect to Neo4j Aura Instance by passing URI and password or using Neo4j credentials file.
2. Choose your source from a list of Unstructured sources to create graph.
3. Change the LLM (if required) from drop down, which will be used to generate graph.
4. Optionally, define schema(nodes and relationship labels) in entity graph extraction settings.
5. Either select multiple files to 'Generate Graph' or all the files in 'New' status will be processed for graph creation.
6. Have a look at the graph for individial files using 'View' in grid or select one or more files and 'Preview Graph'
7. Ask questions related to the processed/completed sources to chat-bot, Also get detailed information about your answers generated by LLM.


## Links

[LLM Knowledge Graph Builder Application](https://llm-graph-builder.neo4jlabs.com/)

[Neo4j Workspace](https://workspace-preview.neo4j.io/workspace/query)

## Reference

[Demo of application](https://www.youtube.com/watch?v=LlNy5VmV290)

## Contact
For any inquiries or support, feel free to raise [Github Issue](https://github.com/neo4j-labs/llm-graph-builder/issues)


## Happy Graph Building!

# JointLK: Joint Reasoning with Language Models and Knowledge Graphs for Commonsense Question Answering

This repo provides the source code & data of our paper: [JointLK: Joint Reasoning with Language Models and Knowledge Graphs for Commonsense Question Answering](https://arxiv.org/abs/2112.02732) (NAACL 2022).

For convenience, all data, checkpoints and codes can be downloaded from my [Baidu Netdisk](https://pan.baidu.com/s/1WsEukLdrHELu6q9_qj8NBA?pwd=y5sd).

<p align="center">
  <img src="./figs/model.png" width="600" title="Question answering task" alt="">
</p>

## 1. Dependencies

Run the following commands to create a conda environment (assuming CUDA11):
```bash
conda create -n jointlk python=3.7
source activate jointlk
pip install torch==1.7.1+cu110 -f https://download.pytorch.org/whl/torch_stable.html
pip install transformers==3.2.0
pip install nltk spacy==2.1.6
python -m spacy download en
# for torch-geometric
pip install torch-cluster==1.5.9 -f https://pytorch-geometric.com/whl/torch-1.7.1+cu110.html
pip install torch-spline-conv==1.2.1 -f https://pytorch-geometric.com/whl/torch-1.7.1+cu110.html
pip install torch-scatter==2.0.6 -f https://pytorch-geometric.com/whl/torch-1.7.1+cu110.html
pip install torch-sparse==0.6.9 -f https://pytorch-geometric.com/whl/torch-1.7.1+cu110.html
pip install torch-geometric==1.6.3 -f https://pytorch-geometric.com/whl/torch-1.7.1+cu110.html
```
See the file env.yaml for all environment dependencies.

## 2. Download Data
We use preprocessed data from the [QA-GNN](https://github.com/michiyasunaga/qagnn) repository, which can also be downloaded from my [Baidu Netdisk](https://pan.baidu.com/s/1haczfYKB1LlgYZ5MYxMDxQ?pwd=x5sl).

The data file structure will look like:

```plain
.
├── data/
    ├── cpnet/                 (prerocessed ConceptNet)
    ├── csqa/
        ├── train_rand_split.jsonl
        ├── dev_rand_split.jsonl
        ├── test_rand_split_no_answers.jsonl
        ├── statement/             (converted statements)
        ├── grounded/              (grounded entities)
        ├── graphs/                (extracted subgraphs)
        ├── ...
    ├── obqa/
    ├── medqa_usmle/
    └── ddb/
```


## 3. Training JointLK
(Assuming slurm job scheduling system)

For CommonsenseQA, run
```
sbatch sbatch_run_jointlk__csqa.sh
```
For OpenBookQA, run
```
sbatch sbatch_run_jointlk__obqa.sh
```

## 4. Pretrained model checkpoints
CommonsenseQA
<table>
  <tr>
    <th>Trained model</th>
    <th>In-house Dev acc.</th>
    <th>In-house Test acc.</th>
  </tr>
  <tr>
    <th>RoBERTa-large + JointLK <a href="https://pan.baidu.com/s/1rGLPwgwdDd92PvxKgCj8Ug?pwd=adqz">[link]</a></th>
    <th>77.6</th>
    <th>75.3</th>
  </tr>
  <tr>
    <th>RoBERTa-large + JointLK <a href="https://pan.baidu.com/s/10jBkJmN_aAf6FIuSSAESPQ?pwd=4un7">[link]</a></th>
    <th>78.4</th>
    <th>74.2</th>
  </tr>
</table>

OpenBookQA
<table>
  <tr>
    <th>Trained model</th>
    <th>Dev acc.</th>
    <th>Test acc.</th>
  </tr>
  <tr>
    <th>RoBERTa-large + JointLK <a href="https://pan.baidu.com/s/1L8K_DWEPjfpXQ54f6iO8uA?pwd=8bjb">[link]</a></th>
    <th>68.8</th>
    <th>70.4</th>
  </tr>
  <tr>
    <th>AristoRoBERTa-large + JointLK <a href="https://pan.baidu.com/s/17ChzwWw_3fAwvmsD3wFgQg?pwd=23hr">[link]</a></th>
    <th>79.2</th>
    <th>85.6</th>
  </tr>
</table>


## 5. Evaluating a pretrained model checkpoint
For CommonsenseQA, run
```
sbatch sbatch_run_jointlk__csqa_test.sh
```
For OpenBookQA, run
```
sbatch sbatch_run_jointlk__obqa_test.sh
```


## 6. Acknowledgment
This repo is built upon the following work:
```
QA-GNN: Question Answering using Language Models and Knowledge Graphs
https://github.com/michiyasunaga/qagnn
```
Many thanks to the authors and developers!

## Others
We noticed that the [QA-GNN](https://github.com/michiyasunaga/qagnn) repository added test results on the MedQA dataset. To facilitate future researchers to compare different models, we also test the performance of JointLK on MedQA.

For training MedQA, run
```
sbatch sbatch_run_jointlk__medqa_usmle.sh
```
for testing MedQA, run
```
sbatch sbatch_run_jointlk__medqa_usmle_test.sh
```


A pretrained model checkpoint
<table>
  <tr>
    <th>Trained model</th>
    <th>Dev acc.</th>
    <th>Test acc.</th>
  </tr>
  <tr>
    <th>SapBERT-base + JointLK <a href="https://pan.baidu.com/s/1UDCew4dkm-iTA24vko3uGA?pwd=crub">[link]</a></th>
    <th>38.0 </th>
    <th>39.8 </th>
  </tr>
</table>



