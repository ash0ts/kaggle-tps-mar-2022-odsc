from prefect.run_configs import LocalRun, RunConfig, VertexRun, DockerRun
from prefect.storage.github import GitHub
from prefect.client.secrets import Secret
from prefect import Parameter
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

# TODO: Set environment from secrets not environment variables anymore
competition = Parameter(
    "competition", default="tabular-playground-series-mar-2022")
project_name = Parameter(
    "project_name", default="kaggle-tps-mar-2022-odsc")
num_experiments = Parameter(
    "num_experiments", default=3)

# TODO: Remove hardcoded image names
# TODO: Better management of passed secrets/environ variables base on conditions


def set_run_config(RUN_TYPE: str = "local") -> RunConfig:
    KAGGLE_USERNAME = os.environ["KAGGLE_USERNAME"]
    KAGGLE_KEY = os.environ["KAGGLE_KEY"]
    WANDB_API_KEY = os.environ["WANDB_API_KEY"]

    env = {
        "KAGGLE_USERNAME": KAGGLE_USERNAME,
        "KAGGLE_KEY": KAGGLE_KEY,
        "WANDB_API_KEY": WANDB_API_KEY,
        "GITHUB_FLOW_REPO": os.environ["GITHUB_FLOW_REPO"],
        "GITHUB_ACCESS_TOKEN": os.environ["GITHUB_ACCESS_TOKEN"]
    }

    if RUN_TYPE == "local":
        return LocalRun(labels=["dev"], env=env)
    elif RUN_TYPE == "docker":
        return DockerRun(labels=["dev"], env=env, image="pycaret-prefect-wandb")
    elif RUN_TYPE == "vertext":
        return VertexRun(
            labels=["prod"],
            image=f"us-east1-docker.pkg.dev/automltabular/kaggle-auto-ml-tps/pycaret-prefect-wandb:latest",
            image_pull_policy="IfNotPresent",
            env=env
        )
    else:
        raise ValueError("Run type not proper!")


def set_storage(flow_name: str) -> GitHub:
    GITHUB_FLOW_REPO = os.environ["GITHUB_FLOW_REPO"]
    GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]

    return GitHub(
        repo=GITHUB_FLOW_REPO,
        path=f"src/{flow_name}.py",
        access_token_secret=GITHUB_ACCESS_TOKEN,
    )
