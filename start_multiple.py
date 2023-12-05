import subprocess

# Define the parameters for your_script.py
camera_names = ["camera1", "camera2", "camera3", "camera4"]
rtsp_urls = [
    "rtsp://camera1_ip_address:554/1/h264major",
    "rtsp://camera2_ip_address:554/1/h264major",
    "rtsp://camera3_ip_address:554/1/h264major",
    "rtsp://camera4_ip_address:554/1/h264major",
]

# Loop through the parameters and start your_script.py for each combination
for camera_name, rtsp_url in zip(camera_names, rtsp_urls):
    command = [
        "python",
        "detect.py",
        "--camera_name",
        camera_name,
        "--rtsp_url",
        rtsp_url
    ]
    
    # Run the command in a subprocess
    subprocess.run(command)
