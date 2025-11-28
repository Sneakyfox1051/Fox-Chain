#!/usr/bin/env python3
"""
Chain Explorer - Blockchain Data Analytics
Startup script for the Flask application
"""

import os
import sys
from dotenv import load_dotenv
from app import app

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Check if data file exists
    data_file = os.getenv('DATA_FILE', 'combined_block.csv')
    if not os.path.exists(data_file):
        print(f"❌ Error: {data_file} not found!")
        print("Please make sure you have blockchain data in the current directory.")
        sys.exit(1)
    
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting Chain Explorer - Blockchain Data Analytics")
    print(f"📊 Dashboard: http://localhost:{port}")
    print(f"📈 Analytics: http://localhost:{port}/analytics")
    print(f"🔧 Debug Mode: {'ON' if debug else 'OFF'}")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=debug, host=host, port=port)
