import wandb
from prefect import task, Flow
from prefect.executors import LocalExecutor
from kaggle.api.kaggle_api_extended import KaggleApi
from flow_utilities import add_convert_for_wandb
from zipfile import ZipFile
import os
from flow_utilities import competition, project_name, set_storage, set_run_config

# TODO: Have switch to turn off prefect task given condition
# TODO: Split into collection of digestible tasks and let a run encapsulate a flow?
KAGGLE_USERNAME = os.environ["KAGGLE_USERNAME"]
KAGGLE_KEY = os.environ["KAGGLE_KEY"]


@task(log_stdout=True)
def download_and_log_kaggle_data(competition: str = "tabular-playground-series-mar-2022", project_name: str = "kaggle-tps-mar-2022-odsc"):

    # logger = prefect.context.get("logger")

    print(f"starting new run for {project_name}")
    run = wandb.init(
        project=project_name, job_type="download", name=f"log-{competition}")

    api = KaggleApi()
    api.authenticate()
    api.competition_download_files(competition)
    zip_path = f"{competition}.zip"
    path_to_raw = os.path.join(".", "data", "raw")
    ZipFile(zip_path).extractall(path=path_to_raw)
    os.remove(zip_path)

    # TODO: Remove hack to add data secription
    if competition == "tabular-playground-series-mar-2022":
        data_description = """
            In this competition, you'll forecast twelve-hours of traffic flow in a major U.S. metropolitan area. Time, space, and directional features give you the chance to model interactions across a network of roadways.

            Files and Field Descriptions
            -------------------------------
            train.csv - the training set, comprising measurements of traffic congestion across 65 roadways from April through September of 1991.
            row_id - a unique identifier for this instance
            time - the 20-minute period in which each measurement was taken
            x - the east-west midpoint coordinate of the roadway
            y - the north-south midpoint coordinate of the roadway
            direction - the direction of travel of the roadway. EB indicates "eastbound" travel, for example, while SW indicates a "southwest" direction of travel.
            congestion - congestion levels for the roadway during each hour; the target. The congestion measurements have been normalized to the range 0 to 100.
            test.csv - the test set; you will make hourly predictions for roadways identified by a coordinate location and a direction of travel on the day of 1991-09-30.
            sample_submission.csv - a sample submission file in the correct format
        """

    raw_data_artifact = wandb.Artifact(
        name="raw", type=competition, description=data_description)
    add_convert_for_wandb(raw_data_artifact, path_to_raw)

    run.log_artifact(raw_data_artifact)
    run.finish()

    return None

# TODO: Abstract away the project name for the flow


def configure_flow(FLOW_NAME: str = "1_download_and_log_kaggle_data", RUN_TYPE: str = "local"):
    with Flow(FLOW_NAME,
              #   executor=LocalExecutor(),
              storage=set_storage(FLOW_NAME),
              run_config=set_run_config(RUN_TYPE)) as flow:
        flow.add_edge(competition, download_and_log_kaggle_data)
        flow.add_edge(project_name, download_and_log_kaggle_data)

    flow.register(project_name="odsc-east-2022")

    return flow


if __name__ == "__main__":
    flow = configure_flow()
