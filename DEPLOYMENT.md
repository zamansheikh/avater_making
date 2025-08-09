# Avatar Processing Backend

## Quick Start Guide

### 1. Automatic Setup (Recommended)
```bash
python setup.py
```

### 2. Manual Setup

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Installation Steps

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run Django setup:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser  # Optional
   ```

6. **Start the server:**
   ```bash
   python manage.py runserver
   ```

## API Usage

### Upload and Process Avatar

**Endpoint:** `POST /api/process-avatar/`

**Request:**
```bash
curl -X POST \
  http://localhost:8000/api/process-avatar/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@/path/to/your/image.jpg'
```

**Response:**
```json
{
    "success": true,
    "message": "Avatar processed successfully",
    "processed_image_url": "http://localhost:8000/media/uploads/processed/avatar_123.png",
    "original_filename": "user_photo.jpg",
    "processing_details": {
        "cropped": true,
        "background_removed": true,
        "size": "512x512",
        "original_size_bytes": 2048576,
        "processed_size_bytes": 1024768
    },
    "avatar_id": 123
}
```

### Get Processing Status

**Endpoint:** `GET /api/avatar-status/{avatar_id}/`

```bash
curl http://localhost:8000/api/avatar-status/123/
```

### Health Check

**Endpoint:** `GET /api/health/`

```bash
curl http://localhost:8000/api/health/
```

### API Information

**Endpoint:** `GET /api/info/`

```bash
curl http://localhost:8000/api/info/
```

## Frontend Integration

### JavaScript Example

```javascript
async function uploadAvatar(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    try {
        const response = await fetch('http://localhost:8000/api/process-avatar/', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('Avatar processed:', result.processed_image_url);
            return result;
        } else {
            console.error('Processing failed:', result.error);
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Upload failed:', error);
        throw error;
    }
}

// Usage
const fileInput = document.getElementById('avatar-upload');
fileInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file) {
        try {
            const result = await uploadAvatar(file);
            // Display the processed avatar
            document.getElementById('avatar-preview').src = result.processed_image_url;
        } catch (error) {
            alert('Avatar processing failed: ' + error.message);
        }
    }
});
```

### React Example

```jsx
import React, { useState } from 'react';

function AvatarUploader() {
    const [uploading, setUploading] = useState(false);
    const [avatarUrl, setAvatarUrl] = useState(null);
    const [error, setError] = useState(null);

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('http://localhost:8000/api/process-avatar/', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                setAvatarUrl(result.processed_image_url);
            } else {
                setError(result.message || 'Processing failed');
            }
        } catch (err) {
            setError('Upload failed: ' + err.message);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div>
            <input
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                disabled={uploading}
            />
            
            {uploading && <p>Processing avatar...</p>}
            {error && <p style={{color: 'red'}}>Error: {error}</p>}
            {avatarUrl && (
                <img 
                    src={avatarUrl} 
                    alt="Processed Avatar" 
                    style={{width: '200px', height: '200px'}}
                />
            )}
        </div>
    );
}

export default AvatarUploader;
```

## Configuration

### Environment Variables

Edit `.env` file to customize settings:

```env
# Security
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Upload Settings
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_IMAGE_TYPES=jpg,jpeg,png,webp

# Processing Settings
OUTPUT_IMAGE_SIZE=512
BACKGROUND_REMOVAL=True
AUTO_CROP=True

# CORS (for frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Features

### ✨ Image Processing Features
- **Smart Face Detection**: Automatically detects and crops around faces
- **Background Removal**: AI-powered background removal with transparency
- **Image Enhancement**: Automatic color correction and sharpening
- **Format Optimization**: Converts to optimized PNG with transparency
- **Batch Processing**: Handles multiple images efficiently

### 🔒 Security Features
- **File Validation**: Strict file type and size validation
- **Secure Upload**: Protected file handling and storage
- **Input Sanitization**: All inputs are properly sanitized
- **Error Handling**: Comprehensive error handling and logging

### 📊 Monitoring Features
- **Processing Status**: Track processing status in real-time
- **Health Checks**: Monitor system health and dependencies
- **Detailed Logging**: Comprehensive logging for debugging
- **Usage Analytics**: Track uploads and processing statistics

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Install development dependencies
pip install black flake8 isort

# Format code
black .

# Check code style
flake8 .

# Sort imports
isort .
```

### Database Management
```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser
```

## Production Deployment

### Environment Setup
1. Set `DEBUG=False` in `.env`
2. Configure proper `SECRET_KEY`
3. Set up production database (PostgreSQL recommended)
4. Configure static file serving
5. Set up proper media file storage (AWS S3, etc.)

### Sample Production Settings
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

## Troubleshooting

### Common Issues

**1. Import Errors**
- Make sure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

**2. Face Detection Not Working**
- OpenCV may need system dependencies
- On Ubuntu: `sudo apt-get install python3-opencv`

**3. Background Removal Slow**
- First run downloads AI models (~100MB)
- Subsequent runs are much faster

**4. File Upload Errors**
- Check file size limits in settings
- Ensure media directories have write permissions

### Support

For issues and feature requests, please check:
1. Environment configuration in `.env`
2. Dependencies in `requirements.txt`
3. Django logs for detailed error messages
4. Health check endpoint: `/api/health/`
