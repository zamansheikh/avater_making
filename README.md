# Avatar Processing Backend

A professional Django REST API for processing user-uploaded images to create perfect avatars.

## 🚀 Quick Start

**The backend is ready to use!** Server is running at: http://127.0.0.1:8989/

### Test the API:
- **API Info**: http://127.0.0.1:8989/api/info/
- **Health Check**: http://127.0.0.1:8989/api/health/
- **Upload Endpoint**: `POST http://127.0.0.1:8989/api/process-avatar/`

## Features

- **AI-Powered Processing**: Smart face detection and cropping
- **Background Removal**: Automatic background removal with transparency
- **Image Enhancement**: Automatic color correction and sharpening
- **Professional Output**: High-quality PNG avatars with transparency
- **Secure Upload**: File validation and secure handling
- **Real-time Processing**: Fast processing with status tracking

## API Endpoints

### Upload and Process Avatar
```
POST /api/process-avatar/
```

**Request Example:**
```bash
curl -X POST \
  http://127.0.0.1:8989/api/process-avatar/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@/path/to/your/image.jpg'
```

**Response:**
```json
{
    "success": true,
    "message": "Avatar processed successfully",
    "processed_image_url": "http://127.0.0.1:8989/media/uploads/processed/avatar_123.png",
    "original_filename": "user_photo.jpg",
    "processing_details": {
        "cropped": true,
        "background_removed": true,
        "face_detected": true,
        "size": "512x512",
        "original_size_bytes": 2048576,
        "processed_size_bytes": 1024768
    },
    "avatar_id": 123
}
```

## Frontend Integration

### JavaScript Example
```javascript
const formData = new FormData();
formData.append('image', imageFile);

fetch('http://127.0.0.1:8989/api/process-avatar/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Avatar URL:', data.processed_image_url);
        // Display the avatar
        document.getElementById('avatar').src = data.processed_image_url;
    }
});
```

## Installation (Already Complete)

The project is already set up and running. If you need to restart:

```bash
# Start the server
python_run.bat manage.py runserver
```

## Technology Stack

- Django 4.2+
- Django REST Framework
- Pillow (PIL) for image processing
- OpenCV for advanced image processing
- rembg for background removal
- python-dotenv for environment management

## Configuration

Configure the following environment variables in `.env`:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `MEDIA_ROOT`: Path for media files storage
- `MAX_UPLOAD_SIZE`: Maximum file upload size in bytes

## Security Features

- File type validation
- File size limits
- Secure filename handling
- CORS configuration
- Input sanitization
