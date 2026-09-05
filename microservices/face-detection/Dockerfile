# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install any needed dependencies specified in requirements.txt
COPY requirements.txt constraints.txt .
# Apply the ABI constraint to every pip invocation, including later reinstalls.
ENV PIP_CONSTRAINT=/app/constraints.txt
RUN pip install --no-cache-dir -r requirements.txt

# Fix OpenCV conflict by uninstalling opencv-python and keeping only headless version.
# Dependencies are already pinned in requirements.txt, so avoid reinstalling numpy.
RUN pip uninstall -y opencv-python && pip install --force-reinstall --no-deps opencv-python-headless==4.5.2.54

# Copy the application files after installing dependencies so those layers are reusable.
COPY . .
# Fail the image build if binary imports or Flask application startup regress.
RUN python verify_image.py
# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
