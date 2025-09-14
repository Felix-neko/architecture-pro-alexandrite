# Base stage - common_api
FROM python:3.12-slim AS common_api

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy pyproject.toml for dependency installation
COPY pyproject.toml /app

# Install dependencies using uv
RUN uv sync

# Copy common_api
COPY common_api /app/common_api

ENV PYTHONPATH=/app
ENV OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://192.168.16.1:4318/v1/traces

###################
# Child API stage
###################
FROM common_api AS child_api

# Copy child_api.py
COPY child_api /app/child_api

# Порт 100001
CMD ["uv", "run", "python", "child_api/child_api.py"]


####################
# Parent API stage
####################
FROM common_api AS parent_api

# Copy parent_api files
COPY parent_api /app/parent_api

ENV CHILD_API_URL=http://192.168.16.1:10001

# Set the command to run parent_api
# Порт 10000
CMD ["uv", "run", "python", "parent_api/parent_api.py"]


