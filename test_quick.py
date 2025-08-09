import requests
import json

def test_api():
    """Test the avatar processing API"""
    
    print("🧪 Testing Avatar Processing API...")
    print("=" * 50)
    
    # Test API info endpoint
    try:
        print("📋 Testing API Info endpoint...")
        response = requests.get('http://127.0.0.1:8000/api/info/')
        if response.status_code == 200:
            print("✅ API Info endpoint working!")
            data = response.json()
            print(f"   API Name: {data.get('name')}")
            print(f"   Version: {data.get('version')}")
        else:
            print(f"❌ API Info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API Info error: {e}")
    
    print()
    
    # Test health endpoint
    try:
        print("🏥 Testing Health endpoint...")
        response = requests.get('http://127.0.0.1:8000/api/health/')
        if response.status_code == 200:
            print("✅ Health endpoint working!")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Services: {list(data.get('services', {}).keys())}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print()
    print("🎭 API is ready for avatar processing!")
    print("🌐 Demo available at: http://localhost:3000/demo.html")
    print("📝 Upload endpoint: POST http://127.0.0.1:8000/api/process-avatar/")

if __name__ == "__main__":
    test_api()
