FROM ubuntu:18.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev

# set the working directory

WORKDIR /app

# Clone the OpenCV repository
RUN git clone https://github.com/marianosin/stocksFlaskAPI.git

# Set the working directory
WORKDIR /app/stocksFlaskAPI

# Install the required packages
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5000

# Create the database
RUN python main.py

CMD [ "python", "run.py" ]