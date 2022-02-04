#
# OrderMe Dockerfile
#

# Pull base image
FROM python:3.4.5-slim

# Get custom packages
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gcc \
    python3-dev \
    mongodb

# Make local directory
RUN mkdir /qrapp

# Set orderme as the working directory from which CMD, RUN, ADD references
WORKDIR /qrapp

# Copy all files
ADD . .

# Install the local requirements
RUN pip install -r requirements.txt

# Listen to port 5000 at runtime
EXPOSE 5000

# Start the app server
CMD python application.py