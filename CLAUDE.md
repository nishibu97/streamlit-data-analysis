# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based data analysis dashboard for a generative AI Proof of Concept. The project is written in Japanese and designed for interactive data visualization and analysis with potential AI integration.

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start Streamlit application
streamlit run app.py

# Use alternative port if 8501 is busy
streamlit run app.py --server.port 8502
```

### Troubleshooting
```bash
# Check Streamlit version
streamlit version

# Upgrade Streamlit
pip install --upgrade streamlit
```

## Project Structure

This is a minimal Streamlit project currently containing:
- `README.md`: Japanese documentation with setup instructions
- `requirements.txt`: Python dependencies including Streamlit, Pandas, Plotly, Matplotlib, Seaborn
- Planned structure includes:
  - `app.py`: Main application file (not yet created)
  - `data/`: Test data directory  
  - `components/`: UI components
  - `utils/`: Utility functions

## Technology Stack

- **Python 3.8+**: Base language
- **Streamlit**: Web application framework
- **Pandas**: Data analysis and processing
- **Plotly/Matplotlib/Seaborn**: Data visualization
- **NumPy**: Numerical computing

## Development Notes

- Code should follow PEP 8 standards
- Functions and classes should include proper docstrings
- The project is currently in early setup phase with only README and requirements defined
- Main application entry point should be `app.py` when created
- Japanese language is used in documentation and likely in UI components