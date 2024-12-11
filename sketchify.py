import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image

st.set_page_config(page_title="Sketchify - Image to Sketch Converter", layout="wide")

# CSS for footer positioning
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 12px;
            right: 20px;
            color: gray;
            font-size: 0.9em;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Set page title and layout
    st.title("Sketchify - Image to Sketch Converter 🖼️")
    st.markdown("Easily transform your images into beautiful pencil sketches with this intuitive app. Just upload your photo and watch as it turns into a stunning sketch in seconds!")
    st.markdown("---")

    # Add a sidebar for instructions and settings
    with st.sidebar:
        # Main file uploader
        st.markdown("---")
        st.header("📜 Instructions")
        st.write("1. Upload an image (JPEG, PNG, or JPG).\n"
                 "2. The app will convert it into a pencil sketch.\n"
                 "3. View the original and sketch side by side.")
        st.write("🎨 **Tip:** Use high-quality images for better results.")
        st.write("Developed with ❤️ using OpenCV and Streamlit.")
    
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:

        # Load the image
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        # Extract the base filename without extension
        file_name = os.path.splitext(uploaded_file.name)[0]

        # Check if the image is grayscale
        if len(image_np.shape) == 2 or image_np.shape[2] == 1:
            st.warning("The uploaded image is already grayscale. Please upload a color image for better results.")
            return

        # Convert to BGR for OpenCV processing
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Grayscale conversion
        gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        # Invert grayscale image
        inverted_gray_image = cv2.bitwise_not(gray_image)

        # Gaussian Blur
        blurred_image = cv2.GaussianBlur(inverted_gray_image, (111, 111), 0)

        # Invert the blurred image
        inverted_blurred_image = cv2.bitwise_not(blurred_image)

        # Create the pencil sketch
        pencil_sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

        # Create a side-by-side layout for images
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📸 Original Image")
            st.image(image, caption="Uploaded Image")

        with col2:
            st.subheader("✏️ Pencil Sketch")
            st.image(pencil_sketch, caption="Pencil Sketch", channels="GRAY")

        # Add a download button for the sketch
        sketch_pil = Image.fromarray(pencil_sketch)
        sketch_pil.save("sketch.png")
        with open("sketch.png", "rb") as file:
            st.download_button("📥 Download Sketch", data=file, file_name=f"{file_name}_sketch.png", mime="image/png")
        st.markdown("---")
    
    
    st.markdown("<div class='footer'>Powered by Luzy | Sketchify </div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
