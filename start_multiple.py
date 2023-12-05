import subprocess

# Define the parameters for your_script.py
camera_names = ["Bug", "Heck", "Backboard", "Steuerboard"]
rtsp_urls = [
    "rtsp://192.168.237.1:5541/0554eebe-d674-46b2-b7c4-df88dac3aa2e/0",
    "rtsp://192.168.237.1:5541/54bd800f-4ebb-43ad-a3e0-cf5258c8d7cc/0",
    "rtsp://192.168.237.1:5541/45e9c602-a351-4395-82d1-e514323da00f/0",
    "rtsp://192.168.237.1:5541/ea180e4c-266f-425e-9163-5e3ffc94fd88/0"
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
