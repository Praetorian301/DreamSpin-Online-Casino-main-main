"""
DreamSpin Casino - Main Application Entry Point
Run this file to start the server: python run.py
"""
import os
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Run the application
    print("🎰 Starting DreamSpin Casino...")
    print("📍 Server running at: http://127.0.0.1:5000")
    print("🛑 Press CTRL+C to stop")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )