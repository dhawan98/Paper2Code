import streamlit as st
import requests
import tempfile

st.title("📄 Technical Paper Implementer")

# File uploader for research paper
uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.success("PDF Uploaded Successfully! Extracting key insights...")

    # Send file to API for processing
    with open(temp_path, "rb") as file:
        response = requests.post("http://127.0.0.1:8000/extract", files={"file": file})

    if response.status_code == 200:
        data = response.json()

        # Display key insights
        st.subheader("📌 Key Insights")
        for key, value in data["insights"].items():
            st.write(f"**{key}**: {value}")

        # Display generated code
        st.subheader("🖥️ Generated Code")
        st.code(data["code"], language="python")

        # Display required libraries
        st.subheader("📦 Required Libraries")
        if data["libraries"]:
            st.write("The following libraries are needed for this implementation:")
            st.code("\n".join(data["libraries"]), language="plaintext")
        else:
            st.warning("No external libraries detected.")

        # Download requirements.txt
        if "requirements" in data:
            st.download_button("📥 Download requirements.txt", data["requirements"], file_name="requirements.txt")

        # Setup instructions
        st.subheader("⚙️ Setup Instructions")
        setup_instructions = f"""
        1. **Create a Virtual Environment**  
           ```bash
           python -m venv paper_venv
           source paper_venv/bin/activate  # On Windows: paper_venv\\Scripts\\activate
           ```

        2. **Install Dependencies**  
           ```bash
           pip install -r requirements.txt
           ```

        3. **Run the Script**  
           ```bash
           python script.py
           ```
        """
        st.markdown(setup_instructions)

        # Display code explanation
        st.subheader("📖 Code Explanation")
        st.write(data["explanation"])

    else:
        st.error("Error processing the paper. Please try again.")
