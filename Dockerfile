
# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /main

# Copy the application files to the container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the application (if applicable)
EXPOSE 8000

# Define the command to run the application
CMD ["python", "main.py"]
