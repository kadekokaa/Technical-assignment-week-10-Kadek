import cv2
import numpy as np
import requests
import random 

TOKEN = "BBFF-E7TPIZuiXdaKOS3gELBZPWRUtsRxKJ"
DEVICE_LABEL = "SIC"
JUMLAH_BARANG = "jumlah barang"
JUMLAH_BARANG_ungu = "jumlah barang ungu"
SUHU_RUANG="temperature room"

# Define the color ranges you want to detect (e.g., blue and green)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_purple = np.array([140, 50, 50])
upper_purple = np.array([170, 255, 255])
def kirim():
    #ubidots send
    temperature_value = round(random.uniform(-10, 50), 2)
     
    payload = {
        JUMLAH_BARANG: blue_object_count,
        JUMLAH_BARANG_ungu: green_object_count,
        SUHU_RUANG : temperature_value 
    }

    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    try:
        response = requests.post(url=url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Data sent to Ubidots: biru={blue_object_count} ungu:{green_object_count} suhu :{temperature_value}")
        else:
            print("Failed to send data. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)
# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 indicates the default camera (usually the laptop's built-in camera)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks to isolate the blue and green colors
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_purple, upper_purple)

    # Combine the masks to detect both blue and green objects
    combined_mask = mask_blue + mask_green

    # Find contours in the combined mask
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize counters for blue and green objects
    blue_object_count = 0
    green_object_count = 0

    # Loop through detected contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # Filter out small noise by setting a threshold for the area
        if area > 100:
            # Draw a bounding box around the detected object
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Determine the color of the object based on which mask it matched
            if mask_blue[y + h // 2, x + w // 2] == 255:
                color = "Blue"
                blue_object_count += 1
            elif mask_green[y + h // 2, x + w // 2] == 255:
                color = "Green"
                green_object_count += 1

            # Display the color of the detected object
            cv2.putText(frame, f'{color} Object', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the frame with objects and the count of each color
    cv2.putText(frame, f'Blue Objects: {blue_object_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Green Objects: {green_object_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Color Detection', frame)
    kirim()
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

# Print the final count of blue and green objects
print("Total Blue Objects Detected:", blue_object_count)
print("Total Green Objects Detected:", green_object_count) 
