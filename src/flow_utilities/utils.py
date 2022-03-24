import os
import pandas as pd
import wandb
from pandas_profiling import ProfileReport
os.environ["PYTHONUTF8"] = "1"


def add_convert_for_wandb(artifact, path, profile=True):

    artifact.add_dir(path, name="data")

    for file_name in os.listdir(path):
        if file_name.endswith(".csv"):
            path_to_file = os.path.join(path, file_name)
            tab_name = file_name.replace(".csv", "")
            print(f"adding {tab_name}")
            df = pd.read_csv(path_to_file)
            print(f"{tab_name}:{df.shape}")
            table = wandb.Table(dataframe=df)
            artifact.add(table, name=tab_name)

            if profile:
                # The output of the profile report will be an HTML which we will log to W&B under the artifact made
                data_profile = ProfileReport(
                    df, dark_mode=True, title=tab_name, minimal=True)
                profile_path = f"{tab_name}.html"
                data_profile.to_file(profile_path)
                data_table_profile = wandb.Html(profile_path)
                artifact.add(data_table_profile, f"{tab_name}_profile")
                # artifact.add_file(profile_path)

    return None
