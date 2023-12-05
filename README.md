# yolov5_mqtt
Docker container for object detection with Yolov5 and broadcasting the detection with MQTT

# Usage

1. Build the Docker image:

```bash
docker build -t yolov5-mqtt .
```

2. Run the Docker container:

```bash
docker run -it yolov5-mqtt
```

# Parameters

Change the following parameters in detect.py to suit your needs:

```python
# MQTT server configuration
mqtt_broker = "mqtt.eclipse.org"
mqtt_port = 1883
mqtt_username = "your_mqtt_username"
mqtt_password = "your_mqtt_password"
mqtt_topic_prefix = "addix_object_detection_results"

```

and in start_multiple.py:

```python
camera_names = ["camera1", "camera2", "camera3", "camera4"]
rtsp_urls = [
    "rtsp://camera1_ip_address:554/1/h264major",
    "rtsp://camera2_ip_address:554/1/h264major",
    "rtsp://camera3_ip_address:554/1/h264major",
    "rtsp://camera4_ip_address:554/1/h264major",
]
```


Note: Ensure that you have Docker installed and that you have the appropriate permissions to run Docker commands. 