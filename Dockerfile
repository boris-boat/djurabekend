# Base Image 
FROM python:3.9-slim

# Work directory
WORKDIR /app

# Copy dependencies (requirements.txt)
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000  

# Command to start your Flask app
CMD ["python", "djuraserver.py"] 
