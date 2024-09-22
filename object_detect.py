import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Utility function to order the points of the bounding box
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

# Function to calculate the size of the object
def calculate_size(c, pixels_per_metric=None):
    box = cv2.minAreaRect(c)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = order_points(box)

    (tl, tr, br, bl) = box
    width = np.linalg.norm(tr - tl)
    height = np.linalg.norm(bl - tl)

    if pixels_per_metric is not None:
        width = width / pixels_per_metric
        height = height / pixels_per_metric

    return (box, width, height)

# Function to capture and measure from webcam or mobile camera
def measure_from_camera(camera_source, reference_width):
    cap = cv2.VideoCapture(camera_source)
    pixels_per_metric = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(gray_blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            reference_object_contour = contours[0]
            (box, ref_width, ref_height) = calculate_size(reference_object_contour)

            if pixels_per_metric is None:
                pixels_per_metric = ref_width / reference_width

            for c in contours:
                (box, width, height) = calculate_size(c, pixels_per_metric)
                cv2.drawContours(frame, [np.intp(box)], -1, (0, 255, 0), 2)
                text = f"W: {width:.1f} mm, H: {height:.1f} mm"
                cv2.putText(frame, text, (int(box[0][0]), int(box[0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(frame_rgb)
        plt.title("Camera Object Measurement")
        plt.axis('off')
        plt.draw()
        plt.pause(0.01)
        plt.clf()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting camera capture.")
            break

    cap.release()
    plt.close()

# Function to measure from selected images
def measure_from_images(image_dir, reference_width):
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("No images found in the specified directory.")
        return

    # List images for selection
    print("Available images:")
    for i, image_file in enumerate(image_files):
        print(f"{i + 1}: {image_file}")

    # Ask user to select an image
    choice = int(input(f"Select an image by number (1-{len(image_files)}): ")) - 1

    if choice < 0 or choice >= len(image_files):
        print("Invalid choice. Exiting.")
        return

    selected_image = image_files[choice]
    frame = cv2.imread(os.path.join(image_dir, selected_image))
    if frame is None:
        print(f"Failed to load image {selected_image}. Exiting.")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray_blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pixels_per_metric = None

    if contours:
        reference_object_contour = contours[0]
        (box, ref_width, ref_height) = calculate_size(reference_object_contour)

        if pixels_per_metric is None:
            pixels_per_metric = ref_width / reference_width

        for c in contours:
            (box, width, height) = calculate_size(c, pixels_per_metric)
            cv2.drawContours(frame, [np.intp(box)], -1, (0, 255, 0), 2)
            text = f"W: {width:.1f} mm, H: {height:.1f} mm"
            cv2.putText(frame, text, (int(box[0][0]), int(box[0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.imshow(frame_rgb)
    plt.title(f"Image Object Measurement: {selected_image}")
    plt.axis('off')
    plt.show()

# Main function to toggle between webcam, mobile camera, and image input
def main():
    reference_width = 50.0  # Known width of the reference object in mm
    choice = input("Enter 'w' for webcam, 'm' for mobile camera, or 'i' for images: ")

    if choice == 'w':
        measure_from_camera(0, reference_width)  # Local webcam
    elif choice == 'm':
        mobile_ip = input("Enter the IP address of the mobile camera: ")
        measure_from_camera(mobile_ip, reference_width)  # Mobile camera using IP Webcam
    elif choice == 'i':
        image_dir = input("Enter the path to the image directory: ")
        measure_from_images(image_dir, reference_width)
    else:
        print("Invalid choice. Please enter 'w', 'm', or 'i'.")

if __name__ == "__main__":
    main()
