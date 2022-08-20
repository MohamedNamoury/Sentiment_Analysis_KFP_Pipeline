FROM gcr.io/deeplearning-platform-release/base-cu110
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
COPY ./src /pipelines/component/src