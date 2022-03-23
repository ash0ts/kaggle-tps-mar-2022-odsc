FROM prefecthq/prefect:latest-python3.9
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pipenv
ENV PROJECT_DIR /usr/local/src
WORKDIR ${PROJECT_DIR}
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy