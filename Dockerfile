
# Use the official OpenCV image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set the environment variables
ENV PYTHONUNBUFFERED=1

# Run the app when the container starts
CMD ["python", "app.py"]
