# Build frontend
FROM node:18-alpine as frontend-builder
WORKDIR /app/frontend
COPY voc_frontend/package*.json ./
RUN npm install
COPY voc_frontend/ .
RUN npm run build

# Build backend
FROM python:3.9-slim
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY voc_builder/ ./voc_builder/

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./voc_builder/notepad/dist/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Environment variables
ENV EUDIC_ACCESS_KEY=""
ENV STUDY_LIST_ID=""

EXPOSE 8080

# Run the application
CMD ["poetry", "run", "aivoc", "notebook", "--host", "0.0.0.0", "--port", "8080"]
