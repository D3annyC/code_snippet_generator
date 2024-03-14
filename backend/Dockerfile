FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MODEL_NAME mistral

# Run ollama to pull the model
RUN apt-get update && apt-get install -y curl

RUN curl -fsSL https://ollama.com/install.sh -o install_ollama.sh

RUN bash install_ollama.sh

RUN ollama serve

RUN ollama pull $MODEL_NAME
    
# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--reload"]
