import cv2
import numpy as np

def draw_circle(canvas, x, y, size, color):
    """Draw a circle pattern"""
    cv2.circle(canvas, (x, y), size, color, -1)

def draw_square(canvas, x, y, size, color):
    """Draw a square pattern"""
    half_size = size // 2
    cv2.rectangle(
        canvas,
        (x - half_size, y - half_size),
        (x + half_size, y + half_size),
        color,
        -1
    )

def draw_diamond(canvas, x, y, size, color):
    """Draw a diamond pattern"""
    points = np.array([
        [x, y - size],
        [x + size, y],
        [x, y + size],
        [x - size, y]
    ])
    cv2.fillPoly(canvas, [points], color)

def draw_cross(canvas, x, y, size, color):
    """Draw a cross pattern"""
    thickness = max(1, size // 3)
    half_length = size
    cv2.line(canvas, (x - half_length, y), (x + half_length, y), color, thickness)
    cv2.line(canvas, (x, y - half_length), (x, y + half_length), color, thickness)

def create_matrix_art(image, dot_size, spacing, intensity, color, bg_color, style="circle"):
    """
    Create matrix art effect from input image.
    
    Args:
        image (np.array): Input image
        dot_size (int): Size of dots
        spacing (int): Spacing between dots
        intensity (float): Effect intensity
        color (tuple): RGB color for the effect
        bg_color (tuple): RGB color for the background
        style (str): Pattern style ("circle", "square", "diamond", "cross")
    
    Returns:
        np.array: Processed image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()

    # Create output canvas with background color
    height, width = gray.shape
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    canvas[:] = bg_color  # Set background color
    
    # Dictionary of drawing functions
    draw_functions = {
        "circle": draw_circle,
        "square": draw_square,
        "diamond": draw_diamond,
        "cross": draw_cross
    }
    
    draw_func = draw_functions.get(style, draw_circle)
    
    # Create pattern
    for y in range(0, height, spacing):
        for x in range(0, width, spacing):
            # Get the average intensity in the region
            if y + spacing < height and x + spacing < width:
                region = gray[y:y + spacing, x:x + spacing]
                avg_intensity = np.mean(region)
                
                # Calculate size based on intensity
                current_size = int(dot_size * (1 - avg_intensity/255) * intensity)
                if current_size > 0:
                    # Draw pattern using selected style
                    draw_func(
                        canvas,
                        x + spacing//2,
                        y + spacing//2,
                        current_size,
                        color
                    )

    # Blend with original image
    result = cv2.addWeighted(
        image,
        1 - intensity,
        canvas,
        intensity,
        0
    )
    
    return result
