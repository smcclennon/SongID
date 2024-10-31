# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install Git
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY app .

# Command to run your application
CMD ["python", "SongID.py"]
