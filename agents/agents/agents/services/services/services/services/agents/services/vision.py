
import cv2
import numpy as np


def analyze_image(image_path):

    if not image_path:
        return {
            "error": "Please upload an image."
        }

    try:
        # Read uploaded image
        image = cv2.imread(image_path)

        if image is None:
            return {
                "error": "Unable to read uploaded image."
            }

        # Image dimensions
        height, width = image.shape[:2]

        # Convert to grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # Detect edges
        edges = cv2.Canny(
            gray,
            threshold1=100,
            threshold2=200
        )

        # Calculate image brightness
        brightness = float(np.mean(gray))

        # Detect basic color information
        average_color = np.mean(
            image,
            axis=(0, 1)
        ).astype(int)

        # Count edge pixels
        edge_pixels = int(
            np.count_nonzero(edges)
        )

        edge_percentage = round(
            edge_pixels / (height * width) * 100,
            2
        )

        return {
            "status": "Image processed successfully",
            "image_width": width,
            "image_height": height,
            "brightness": round(brightness, 2),
            "average_color_bgr": average_color.tolist(),
            "edge_percentage": edge_percentage,
            "processing": [
                "Grayscale conversion",
                "Canny edge detection",
                "Brightness analysis",
                "Color analysis"
            ],
            "technology": "OpenCV"
        }

    except Exception as error:
        return {
            "error": str(error)
        }
