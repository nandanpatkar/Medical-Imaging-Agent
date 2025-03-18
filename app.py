import os
from PIL import Image
import pydicom
import numpy as np
from phi.agent import Agent
from phi.model.google import Gemini
import streamlit as st
from phi.tools.duckduckgo import DuckDuckGo

# Initialize session state
if "GOOGLE_API_KEY" not in st.session_state:
    st.session_state.GOOGLE_API_KEY = None

# Initialize analyze_clicked state
if "analyze_clicked" not in st.session_state:
    st.session_state.analyze_clicked = False

def on_analyze_click():
    st.session_state.analyze_clicked = True

def process_dicom(dicom_file):
    """Process DICOM file and convert to PIL Image."""
    try:
        # Read the DICOM file
        ds = pydicom.dcmread(dicom_file)
        
        # Get pixel array and rescale to 8-bit
        pixel_array = ds.pixel_array
        
        # Normalize to 8-bit range
        if pixel_array.max() > 255:
            pixel_array = ((pixel_array - pixel_array.min()) / 
                         (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
        
        # Convert to PIL Image
        return Image.fromarray(pixel_array)
    except Exception as e:
        raise Exception(f"Error processing DICOM file: {str(e)}")

def process_tiff(uploaded_file):
    """Process TIFF file specifically."""
    try:
        # Open directly from the uploaded file
        image = Image.open(uploaded_file)
        
        # Convert to RGB if needed
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        
        # Create a copy in memory to ensure the file is fully loaded
        return image.copy()
    except Exception as e:
        raise Exception(f"Error processing TIFF file: {str(e)}")

def process_uploaded_file(uploaded_file):
    """Process uploaded file based on its format."""
    try:
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        if file_extension in ['dcm', 'dicom']:
            # Save DICOM file temporarily
            temp_path = "temp_dicom_file.dcm"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                image = process_dicom(temp_path)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        elif file_extension in ['tif', 'tiff']:
            image = process_tiff(uploaded_file)
            
        else:  # For other supported formats
            image = Image.open(uploaded_file)
            
            # Convert to RGB if needed
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
        
        return image
    except Exception as e:
        raise Exception(f"Error processing uploaded file: {str(e)}")

# Sidebar Configuration
with st.sidebar:
    st.title("ℹ️ Configuration")
    
    # API Key Configuration
    if not st.session_state.GOOGLE_API_KEY:
        api_key = st.text_input(
            "Enter your Google API Key:",
            type="password"
        )
        st.caption(
            "Get your API key from [Google AI Studio]"
            "(https://aistudio.google.com/apikey) 🔑"
        )
        if api_key:
            st.session_state.GOOGLE_API_KEY = api_key
            st.success("API Key saved!")
            st.rerun()
    else:
        st.success("API Key is configured")
        if st.button("🔄 Reset API Key"):
            st.session_state.GOOGLE_API_KEY = None
            st.rerun()
    
    st.info(
        "This tool provides AI-powered analysis of medical imaging data using "
        "advanced computer vision and radiological expertise."
    )
    st.warning(
        "⚠DISCLAIMER: This tool is for educational and informational purposes only. "
        "All analyses should be reviewed by qualified healthcare professionals. "
        "Do not make medical decisions based solely on this analysis."
    )

# Initialize medical agent with proper error handling
try:
    if st.session_state.GOOGLE_API_KEY:
        medical_agent = Agent(
            model=Gemini(
                api_key=st.session_state.GOOGLE_API_KEY,
                id="gemini-1.5-flash"
            ),
            tools=[DuckDuckGo()],
            markdown=True
        )
    else:
        medical_agent = None
except Exception as e:
    st.error(f"Error initializing Gemini model: {str(e)}")
    medical_agent = None

if not medical_agent:
    st.warning("Please configure your API key in the sidebar to continue")

# Medical Analysis Query
query = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the patient's medical image and structure your response as follows:

### 1. Image Type & Region
- Specify imaging modality (X-ray/MRI/CT/Ultrasound/etc.)
- Identify the patient's anatomical region and positioning
- Comment on image quality and technical adequacy

### 2. Key Findings
- List primary observations systematically
- Note any abnormalities in the patient's imaging with precise descriptions
- Include measurements and densities where relevant
- Describe location, size, shape, and characteristics
- Rate severity: Normal/Mild/Moderate/Severe

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level
- List differential diagnoses in order of likelihood
- Support each diagnosis with observed evidence from the patient's imaging
- Note any critical or urgent findings

### 4. Patient-Friendly Explanation
- Explain the findings in simple, clear language that the patient can understand
- Avoid medical jargon or provide clear definitions
- Include visual analogies if helpful
- Address common patient concerns related to these findings

### 5. Research Context
IMPORTANT: Use the DuckDuckGo search tool to:
- Find recent medical literature about similar cases
- Search for standard treatment protocols
- Provide a list of relevant medical links
- Research any relevant technological advances
- Include 2-3 key references to support your analysis

Format your response using clear markdown headers and bullet points. Be concise yet thorough.
"""

st.title("🏥 Medical Imaging Diagnosis Agent")
st.write("Upload a medical image for professional analysis")

# Create containers for better organization
upload_container = st.container()
image_container = st.container()
analysis_container = st.container()

with upload_container:
    uploaded_file = st.file_uploader(
        "Upload Medical Image",
        type=["jpg", "jpeg", "png", "tiff", "tif", "dcm", "dicom"],
        help="Supported formats: JPG, JPEG, PNG, TIFF, DICOM"
    )

# Initialize variables
image = None
resized_image = None

if uploaded_file is not None:
    with image_container:
        try:
            # Process the uploaded file
            image = process_uploaded_file(uploaded_file)
            
            # Center the image using columns
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if image is not None:
                    # Calculate aspect ratio for resizing
                    width, height = image.size
                    aspect_ratio = width / height
                    new_width = 500
                    new_height = int(new_width / aspect_ratio)
                    resized_image = image.resize((new_width, new_height))
                    
                    st.image(
                        resized_image,
                        caption="Uploaded Medical Image",
                        use_container_width=True
                    )
                    
                    st.button(
                        "🔍 Analyze Image",
                        type="primary",
                        on_click=on_analyze_click,
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    with analysis_container:
        if st.session_state.analyze_clicked:
            if not medical_agent:
                st.error("Please configure your API key before analyzing images.")
            else:
                image_path = "temp_medical_image.png"
                try:
                    # Save image with error handling
                    if resized_image is not None:
                        resized_image.save(image_path, format='PNG')
                        
                        with st.spinner("🔄 Analyzing image... Please wait."):
                            try:
                                response = medical_agent.run(query, images=[image_path])
                                st.markdown("### 📋 Analysis Results")
                                st.markdown("---")
                                st.markdown(response.content)
                                st.markdown("---")
                                st.caption(
                                    "Note: This analysis is generated by AI and should be reviewed by "
                                    "a qualified healthcare professional."
                                )
                            except Exception as e:
                                st.error(f"Analysis error: {str(e)}")
                    else:
                        st.error("Error: Image processing failed")
                except Exception as e:
                    st.error(f"Error saving image: {str(e)}")
                finally:
                    if os.path.exists(image_path):
                        try:
                            os.remove(image_path)
                        except Exception as e:
                            st.warning(f"Could not remove temporary file: {str(e)}")
                            
                # Reset the analyze clicked state
                st.session_state.analyze_clicked = False
else:
    st.info("👆 Please upload a medical image to begin analysis")