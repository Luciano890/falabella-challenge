FROM python:3.13.1-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .
EXPOSE 8000
CMD [ "bash", "scripts/run.sh" ]
# CMD [ "tail", "-f", "/dev/null" ] # For debugging
