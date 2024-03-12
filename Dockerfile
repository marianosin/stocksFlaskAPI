FROM python:3.12

# Install dependencies


# set the working directory
WORKDIR /app

# Clone the repository and checkout the branch
RUN git clone -b test_deployment https://github.com/marianosin/stocksFlaskAPI.git /app

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
EXPOSE 5000

# Create the database
RUN python /app/main.py

CMD python /app/app.py