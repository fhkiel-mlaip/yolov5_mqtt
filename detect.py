import cv2
import argparse
import numpy as np
from yolov5 import load_model, detect
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

def detect_objects(model, image, camera_id):
    # Perform object detection using YOLOv5
    results = detect(model, image)

    # Add camera identifier to each result
    results_with_camera_id = [(camera_id, label, confidence, bbox) for label, confidence, bbox in results]

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
        publish_results(camera_name, results)

        # Display the frame with bounding boxes (optional)
        for result in results:
            _, label, confidence, bbox = result
            x, y, w, h = bbox
            cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (int(x), int(y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow(f'Object Detection - {camera_name}', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Object detection and MQTT publishing script.')
    parser.add_argument('--camera_name', type=str, required=True, help='Name of the camera')
    parser.add_argument('--rtsp_url', type=str, required=True, help='RTSP stream URL')
    args = parser.parse_args()

    # Load YOLOv5 model only once
    yolo_model = load_model(yolo_model)

    # Run the main function with provided arguments
    main(args.camera_name, args.rtsp_url, yolo_model)
