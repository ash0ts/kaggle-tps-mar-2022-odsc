FROM prefecthq/prefect:latest-python3.9
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pipenv
ENV PROJECT_DIR /usr/local/project
WORKDIR ${PROJECT_DIR}
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
#TODO: Remove this as we use prefect github flow
COPY src ${PROJECT_DIR}/src
RUN pipenv install --system --deploy