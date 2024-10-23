# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

# Expose the Flask app port
EXPOSE 8080

# Define environment variables
ENV FLASK_APP=app.py

# Command to run your app using Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
