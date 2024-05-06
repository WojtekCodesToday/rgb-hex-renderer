import cv2
import sys

# allows you to enlargen the frames
scale = 6

# Function to resize a frame to fit within a 20x20 display and return render size
def resize_frame(frame):
    # Set the maximum width or height for resizing
    max_dimension = 20
    
    # Find the width and height of the frame
    height, width = frame.shape[:2]

    # Calculate the scaling factor based on the maximum dimension
    scale_factor = min(max_dimension / width, max_dimension / height) * scale

    # Resize the frame with the calculated scale factor
    resized_frame = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))
    
    return resized_frame, resized_frame.shape[:2]

# Function to convert a frame to monochrome format
def convert_frame_to_monochrome(frame):
    # Convert the frame to monochrome by extracting the red channel
    red_channel = frame[:, :, 2]
    
    # Convert each pixel to a two-digit value indicating the intensity of red
    monochrome_pixels = [f"{red_val:03d}" for red_val in red_channel.flatten()]
    
    # Concatenate the pixels into a single string
    frame_string = ''.join(monochrome_pixels)
    
    return frame_string

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Usage: python main.py <video_file> <output_format>")
    print("Supported output formats: monochrome, hex, rgb")
    exit()

# Open the video file
video_file = sys.argv[1]
output_format = sys.argv[2]

# Check if the output format is valid
if output_format not in ['monochrome', 'hex', 'rgb']:
    print("Error: Invalid output format. Supported output formats: monochrome, hex, rgb")
    exit()

cap = cv2.VideoCapture(video_file)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video file")
    exit()

# Open the text file for writing
output_file = "output.txt"
with open(output_file, 'w') as f:
    # Loop through each frame of the video
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        # If the frame is not read properly, break the loop
        if not ret:
            break
        
        # Resize the frame to fit within a 20x20 display
        resized_frame, render_size = resize_frame(frame)
        
        # Print the recommended rendering size for each frame
        print("Recommended rendering size:", render_size, "(height, width)")
        
        # Convert the frame to the desired format
        if output_format == 'monochrome':
            frame_string = convert_frame_to_monochrome(resized_frame)
        elif output_format == 'hex':
            frame_string = convert_frame_to_hex(resized_frame)
        else:
            frame_string = convert_frame_to_rgb(resized_frame)
        
        # Write the frame string to the text file with a newline character
        f.write(frame_string + '\n')

# Release the video capture object
cap.release()
