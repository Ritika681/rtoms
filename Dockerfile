# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

#Ensure the whole project is copied
COPY . . 
# Copy files to container
#COPY main.py /app/

COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Command to run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
