# Use an official Anaconda runtime as a parent image
FROM python:3.10.10
#latest

# Set the working directory in the container
ENV DIRECTORY=/app
WORKDIR ${DIRECTORY}
#WORKDIR /app

# Download and extract Osmosis
RUN wget https://github.com/openstreetmap/osmosis/releases/download/0.47.1/osmosis-0.47.1.tgz && \
    mkdir osmosis && \
    mv osmosis-0.47.1.tgz osmosis && \
    cd osmosis && \
    tar xvfz osmosis-0.47.1.tgz && \
    rm osmosis-0.47.1.tgz && \
    chmod a+x bin/osmosis

RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y openjdk-11-jdk
RUN apt-get install -y maven

# Copy the environment.yml file into the container at /app
COPY . /app 
#COPY environment.yml .

RUN pip install --no-cache-dir -r environment.txt

#CMD ["bash", "-c", "sleep 2000000"]

# Specify the command to run on container start
CMD ["bash", "-c", "python3"]
#CMD ["python3", "pipeline.py"]