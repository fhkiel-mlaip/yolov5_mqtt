import cv2
import argparse
import torch
import paho.mqtt.client as mqtt

# YOLOv5 model configuration
yolo_model = "best.pt"


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
    
    # Results to JSON format
    results_json =  results.pandas().xyxy[0].to_json(orient="records")

    return results_json

def publish_results(camera_id, results):
    # Publish to MQTT topic
    message_info = mqtt_client.publish(f"captnfoerdeareal/wavelab/optics/addix/{camera_id}", results)
    
    # Check if the message was sent successfully
    if message_info.rc != 0:
        print("Error while sending message")
        # Try to reconnect to the MQTT server
        mqtt_client.reconnect()
        mqtt_client.publish(f"captnfoerdeareal/wavelab/optics/addix/{camera_id}", results) 


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
        results_json = detect_objects(yolo_model, frame, camera_name)

        # Publish detection results to MQTT server
        publish_results(camera_name, results_json)
    

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
    yolo_model.conf = 0.6

    # MQTT Initialization CHANGE TO YOUR SETTINGS
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set("user", "password") # Replace with your MQTT username and password
    mqtt_client.connect("192.168.237.1", 1883, 60)  # Replace with your broker address

    # Run the main function with provided arguments
    main(args.camera_name, args.rtsp_url, yolo_model)
