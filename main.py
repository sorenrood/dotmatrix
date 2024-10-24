import streamlit as st
from PIL import Image
import numpy as np
import io
from image_processor import create_matrix_art
from utils import convert_img_to_bytes

st.set_page_config(
    page_title="Matrix Art Generator",
    layout="wide"
)

def main():
    st.title("Matrix Art Generator")
    st.write("Upload an image and create stunning matrix art effects!")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # Load and display original image
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)

        # Effect parameters
        st.sidebar.header("Effect Parameters")
        
        # Style selection
        style = st.sidebar.selectbox(
            "Pattern Style",
            ["circle", "square", "diamond", "cross"],
            help="Choose the pattern style for the matrix effect"
        )
        
        dot_size = st.sidebar.slider("Pattern Size", 2, 20, 8)
        spacing = st.sidebar.slider("Pattern Spacing", 1, 20, 10)
        intensity = st.sidebar.slider("Effect Intensity", 0.0, 1.0, 0.5)
        color = st.sidebar.color_picker("Effect Color", "#00FF00")
        bg_color = st.sidebar.color_picker("Background Color", "#000000")

        # Convert hex colors to RGB
        color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        bg_color_rgb = tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        # Process image
        try:
            processed_img = create_matrix_art(
                np.array(image),
                dot_size,
                spacing,
                intensity,
                color_rgb,
                bg_color_rgb,
                style
            )

            with col2:
                st.subheader("Matrix Art Effect")
                st.image(processed_img, use_column_width=True)

            # Download button
            if processed_img is not None:
                btn = st.download_button(
                    label="Download Matrix Art",
                    data=convert_img_to_bytes(processed_img),
                    file_name=f"matrix_art_{style}.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

    # Instructions
    with st.expander("How to use"):
        st.write("""
        1. Upload an image using the file uploader
        2. Adjust the effect parameters:
           - Pattern Style: Choose between circle, square, diamond, or cross patterns
           - Pattern Size: Controls the size of individual patterns
           - Pattern Spacing: Controls the space between patterns
           - Effect Intensity: Controls the strength of the effect
           - Effect Color: Choose the color for the matrix effect
           - Background Color: Choose the color for the background
        3. Download the processed image using the download button
        """)

if __name__ == "__main__":
    main()
