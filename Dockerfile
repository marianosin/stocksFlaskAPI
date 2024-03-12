FROM python:3.12

# Install dependencies


# set the working directory

WORKDIR /app

# Clone the OpenCV repository
RUN git clone https://github.com/marianosin/stocksFlaskAPI.git
RUN git checkout test_deployment
# Set the working directory
WORKDIR /app/stocksFlaskAPI

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
# Expose the port


# Create the database
RUN python main.py

CMD python ./app.py