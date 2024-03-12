FROM ubuntu

# Update the package list
RUN apt-get update

# Install dependencies
RUN apt-get install -y software-properties-common

# Add the deadsnakes PPA to your sources list
RUN add-apt-repository ppa:deadsnakes/ppa

# Install Python
RUN apt-get install -y python3.9

# Verify the installation
RUN python3.9 --version

# Set the working directory
WORKDIR /app

# Clone the OpenCV repository
RUN git clone https://github.com/marianosin/stocksFlaskAPI.git

# Set the working directory
WORKDIR /app/stocksFlaskAPI

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Expose the port


# Create the database
RUN python main.py



CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]