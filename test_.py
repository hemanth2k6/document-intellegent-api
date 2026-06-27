import requests
import sys
import os

def test_upload():

    try:
        health_response = requests.get("http://localhost:8000/health", timeout=2)
        print("✅ Server is running!")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server first:")
        print("   uvicorn app.main:app --reload")
        return False
    
    
    pdf_path = "test.pdf"  
    
    if not os.path.exists(pdf_path):
        print(f"❌ Test PDF not found at: {pdf_path}")
        print("Please create a test PDF file first.")
        return False
    
    url = "http://localhost:8000/upload"
    
    try:
        with open(pdf_path, "rb") as f:
            files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            print("✅ Upload successful!")
            print("Response:")
            print(response.json())
            return True
        else:
            print(f"❌ Upload failed with status: {response.status_code}")
            print(response.json())
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Is the server running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing PDF Upload...")
    success = test_upload()
    sys.exit(0 if success else 1)