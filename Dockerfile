FROM python:3.12

# Install dependencies


# set the working directory

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

CMD [ "python", '-m', 'flask', 'run', '--host=0.0.0' ]