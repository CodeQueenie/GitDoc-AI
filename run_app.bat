@echo off
cd /d C:\Users\ncole\GitDoc-AI  # Ensure this points to the correct directory
venv\Scripts\activate  # Activate the virtual environment
streamlit run 🏠_Home.py  # Run the Streamlit app
pause  # Keep the terminal open to see any errors