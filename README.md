# kaggle-tps-mar-2022-odsc
 Using PyCaret, W&B, and Prefect to show how to orchestrate reproducible AutoML experiments on the Tabular Playground Series - March 2022 on Kaggle

## Prefect Instructions
prefect backend cloud
prefect agent docker start -l "LABEL"
access_token_secret (str, optional): The name of a Prefect secret that contains a GitHub access token to use when loading flows from this storage.

## GCP Instructions to build image (Windows)
```
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe

gcloud auth application-default login

gcloud auth configure-docker us-east1-docker.pkg.dev

docker build -t pycaret-prefect-wandb .

docker tag pycaret-prefect-wandb us-east1-docker.pkg.dev/automltabular/kaggle-auto-ml-tps/pycaret-prefect-wandb

docker push us-east1-docker.pkg.dev/automltabular/kaggle-auto-ml-tps/pycaret-prefect-wandb

gcloud artifacts docker images list \
us-east1-docker.pkg.dev/automltabular/kaggle-auto-ml-tps/pycaret-prefect-wandb [--include-tags]

// docker pull us-east1-docker.pkg.dev/automltabular/kaggle-auto-ml-tps/pycaret-prefect-wandb:latest
```