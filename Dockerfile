FROM python:3.9-alpine
LABEL maintainer="apaulin <paulin.anthony@gmail.com>"

ENV WEBEX_TEAMS_ACCESS_TOKEN="your_token"
ENV WEBEX_ROOMS='["Foo", "bar"]'
ENV WEBEX_PEOPLE='["foo@Bar.com", "bar@foo.com"]'
ENV RESULT_PATH = "/tmp/result"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python","-m","pipeline_assistant"]