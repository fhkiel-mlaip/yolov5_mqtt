# Use the official YOLOv5 image as a base
FROM ultralytics/yolov5:latest

# Install additional packages for MQTT compatibility
RUN pip install paho-mqtt

# Set the working directory
WORKDIR /app

# Copy the entry point script to the container
COPY entrypoint.sh /app/entrypoint.sh
COPY src /app

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/start_multiple.py

# Set the entry point for the container
ENTRYPOINT ["/app/start_multiple.sh"]
