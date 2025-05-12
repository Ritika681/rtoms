# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files to container
#COPY main.py /app/

COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


#Ensure the whole project is copied
COPY . . 

# Expose port
EXPOSE 8000

# Command to run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
