import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import io

def main():
    st.title("📄 Document OCR Application")
    st.markdown("Extract text from images using state-of-the-art OCR technology")

    # Sidebar for OCR engine selection
    st.sidebar.header("OCR Settings")
    ocr_engine = st.sidebar.selectbox(
        "Choose OCR Engine",
        ["EasyOCR", "Tesseract"]
    )

    # Language selection
    languages = st.sidebar.multiselect(
        "Select Languages",
        ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
        default=["en"]
    )

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload an image file",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        help="Supported formats: JPG, JPEG, PNG, BMP, TIFF"
    )

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📷 Uploaded Image")
            st.image(image, caption="Uploaded Image", use_column_width=True)

        with col2:
            st.subheader("📝 Extracted Text")

            if st.button("🔍 Extract Text", type="primary"):
                with st.spinner("Extracting text..."):
                    try:
                        if ocr_engine == "EasyOCR":
                            # Convert PIL image to numpy array
                            image_np = np.array(image)

                            # Initialize EasyOCR reader
                            reader = easyocr.Reader(languages, gpu=False)

                            # Extract text
                            results = reader.readtext(image_np)

                            # Format results
                            extracted_text = "\n".join([result[1] for result in results])

                        else:  # Tesseract
                            import pytesseract
                            extracted_text = pytesseract.image_to_string(image)

                        # Display results
                        st.success("✅ Text extraction completed!")
                        st.text_area(
                            "Extracted Text:",
                            value=extracted_text,
                            height=200,
                            help="Copy the text from here"
                        )

                        # Download button
                        st.download_button(
                            label="📥 Download Text",
                            data=extracted_text,
                            file_name="extracted_text.txt",
                            mime="text/plain"
                        )

                        # Statistics
                        st.metric("📊 Character Count", len(extracted_text))
                        st.metric("📊 Word Count", len(extracted_text.split()))

                    except Exception as e:
                        st.error(f"❌ Error during text extraction: {str(e)}")

    # Instructions
    st.markdown("---")
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. **Select OCR Engine**: Choose between EasyOCR (recommended) or Tesseract
    2. **Choose Languages**: Select the languages present in your document
    3. **Upload Image**: Drag and drop or browse for your image file
    4. **Extract Text**: Click the "Extract Text" button to process the image
    5. **Download Results**: Use the download button to save extracted text as a .txt file
    """)

    # About section
    with st.expander("ℹ️ About OCR Technology"):
        st.markdown("""
        **Optical Character Recognition (OCR)** is a technology that converts different types of 
        documents — scanned paper documents, PDF files, or images captured by a camera — into 
        editable and searchable data.

        **EasyOCR Features:**
        - Supports 80+ languages
        - High accuracy for printed text
        - GPU acceleration support
        - Easy Python integration

        **Tesseract Features:**
        - Supports 100+ languages
        - Long-standing OCR solution
        - Good for high-resolution images
        - Configurable preprocessing options
        """)

if __name__ == "__main__":
    main()
