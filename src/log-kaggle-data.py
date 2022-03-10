from dotenv import find_dotenv, load_dotenv
import os
import prefect
from prefect import task, Flow, Parameter
from prefect.run_configs import LocalRun
load_dotenv(find_dotenv())


@task(name="log-kaggle-data-to-wandb")
def download_and_log_kaggle_data(competition: str = "tabular-playground-series-mar-2022"):
    from kaggle.api.kaggle_api_extended import KaggleApi
    from zipfile import ZipFile
    import wandb
    import pandas as pd

    # TODO: Find out why logger is not working
    logger = prefect.context.get("logger")

    project_name = os.environ["PROJECT"]
    logger.info(f"starting new run for {project_name}")
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
        name=competition, type="raw_data", description=data_description)
    raw_data_artifact.add_dir(path_to_raw, name="raw_data")

    for file_name in os.listdir(path_to_raw):
        if file_name.endswith(".csv"):
            path_to_file = os.path.join(path_to_raw, file_name)
            tab_name = file_name.replace(".csv", "")
            logger.info(f"adding {tab_name}")
            df = pd.read_csv(path_to_file)
            table = wandb.Table(dataframe=df)
            raw_data_artifact.add(table, name=tab_name)

    run.log_artifact(raw_data_artifact)
    run.finish()

    return None


def configure_prefect_flow():

    with Flow("log-kaggle-data") as flow:
        competition = Parameter(
            "competition", default="tabular-playground-series-mar-2022")
        download_and_log_kaggle_data(competition=competition)

    project_name = os.environ["PROJECT"]
    # Configure the `PROJECT` environment variable for this flow
    flow.run_config = LocalRun(
        env={"PROJECT": project_name, "KAGGLE_USERNAME": os.environ["KAGGLE_USERNAME"],
             "KAGGLE_KEY": os.environ["KAGGLE_KEY"], "WANDB_API_KEY": os.environ["WANDB_API_KEY"]})

    # Register the flow under the "tutorial" project

    flow.register(project_name=project_name)
    # flow.run()


# TODO: Pass competition and run flow as a cli command
if __name__ == "__main__":
    configure_prefect_flow()
