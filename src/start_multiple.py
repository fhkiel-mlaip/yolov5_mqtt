import multiprocessing
import subprocess
import signal
import sys
import time

# Define the parameters for your_script.py
camera_names = ["Bug", "Heck", "Backboard", "Steuerboard"]
rtsp_urls = [
    "rtsp://192.168.237.1:5541/0554eebe-d674-46b2-b7c4-df88dac3aa2e/0",
    "rtsp://192.168.237.1:5541/54bd800f-4ebb-43ad-a3e0-cf5258c8d7cc/0",
    "rtsp://192.168.237.1:5541/45e9c602-a351-4395-82d1-e514323da00f/0",
    "rtsp://192.168.237.1:5541/ea180e4c-266f-425e-9163-5e3ffc94fd88/0"
]

def run_command(command):
    subprocess.call(command, shell=True)

def handle_keyboard_interrupt(signum, frame):
    print("Keyboard interrupt received. Terminating all processes.")
    for process in processes:
        process.terminate()
    sys.exit(0)

if __name__ == '__main__':
    commands = []
    processes = []
    
        # Loop through the parameters and start your_script.py for each combination
    for camera_name, rtsp_url in zip(camera_names, rtsp_urls):
        commands.append(f"python detect.py --camera_name {camera_name} --rtsp_url {rtsp_url}")
    
    for command in commands:
        process = multiprocessing.Process(target=run_command, args=(command,))
        processes.append(process)
        process.start()
        # Importent for cache load error
        time.sleep(10)
        

    # Set up the keyboard interrupt handler
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)

    for process in processes:
        process.join()