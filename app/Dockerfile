# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Copy requirements.txt to the container at /code/requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code to the container at /code/app
COPY . /code/app

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]