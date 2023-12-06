import cv2
import argparse
import numpy as np
import torch
import paho.mqtt.publish as publish

# YOLOv5 model configuration
yolo_model = "best.pt"

# MQTT server configuration
mqtt_broker = "mqtt.eclipse.org"
mqtt_port = 1883
mqtt_username = "your_mqtt_username"
mqtt_password = "your_mqtt_password"
mqtt_topic_prefix = "addix_object_detection_results"

# Provide authentication credentials for MQTT server
auth = {'username': mqtt_username, 'password': mqtt_password}

# Class names
object_types = [
    "SEAMARK", "CARDINAL", "OBSTACLE", "LANDING", "RIB", "MOTORBOAT", "YACHT",
    "DINGHY", "SAILBOAT", "TALLSHIP", "SWIMMER", "ROWER", "CANOE", "SUP",
    "WINDSURFER", "KITEBOARDER", "SKIING", "FERRY", "CRUISE", "CONTAINER",
    "TANKER", "FISHING", "RESEARCH", "OFFSHORE", "DREDGER", "PILOT", "POLICE",
    "MILITARY", "SUBMARINE", "TUG", "PONTOON"
]

def detect_objects(model, image, camera_id):
    # Perform object detection using YOLOv5
    results = model(image, size=1280)

    # Add camera identifier to each result
    results_with_camera_id  = []
    if results.xyxy[0] is not None:
        results_with_camera_id = [(camera_id, object_types[int(label)], confidence, xmin, ymin, xmax, ymax) for xmin, ymin, xmax, ymax, confidence, label in results.xyxy[0].cpu().numpy()]
    
    # Results to JSON format
    # results.pandas().xyxy[0].to_json(orient="records")

    return results_with_camera_id

def publish_results(camera_id, results):
    # Convert results to a JSON format and publish to MQTT server
    topic = f"{mqtt_topic_prefix}/{camera_id}"
    message = {"objects": results}
    publish.single(topic, payload=str(message), hostname=mqtt_broker, port=mqtt_port, auth=auth)

def main(camera_name, rtsp_url, yolo_model):
    # Open RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    while True:
        # Read frame from the RTSP stream
        ret, frame = cap.read()

        if not ret:
            print(f"Failed to retrieve frame for camera {camera_name}.")
            break

        # Perform object detection
        results = detect_objects(yolo_model, frame, camera_name)

        # Publish detection results to MQTT server
        # publish_results(camera_name, results)
        
        # Test print detection and frame information
        print(f"Camera: {camera_name}")
        print(f"Detection results: {results}")
        print(f"Frame shape: {frame.shape}")


    # Release the capture object and close all windows
    cap.release()


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Object detection and MQTT publishing script.')
    parser.add_argument('--camera_name', type=str, required=True, help='Name of the camera')
    parser.add_argument('--rtsp_url', type=str, required=True, help='RTSP stream URL')
    args = parser.parse_args()

    # Load YOLOv5 model only once
    yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path="best.pt", trust_repo=True).eval().to('cuda')
    yolo_model.conf = 0.5

    # Run the main function with provided arguments
    main(args.camera_name, args.rtsp_url, yolo_model)
