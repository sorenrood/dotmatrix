import cv2
import numpy as np
from PIL import Image
import io

def convert_img_to_bytes(image):
    """
    Convert numpy array image to bytes for download.
    
    Args:
        image (np.array): Input image
    
    Returns:
        bytes: Image converted to bytes
    """
    # Convert numpy array to PIL Image
    if isinstance(image, np.ndarray):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Save image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    
    return img_bytes
