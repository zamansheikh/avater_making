"""
Advanced Image Processing Service for Avatar Creation

This service provides comprehensive image processing capabilities including:
- Smart face detection and cropping
- Background removal with transparency
- Image optimization and resizing
- Format conversion and quality enhancement
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
import io
import logging
from typing import Tuple, Optional, Dict, Any
from django.conf import settings

logger = logging.getLogger(__name__)


class AvatarProcessor:
    """Professional avatar processing with AI-powered enhancements"""
    
    def __init__(self):
        self.output_size = getattr(settings, 'OUTPUT_IMAGE_SIZE', 512)
        self.background_removal = getattr(settings, 'BACKGROUND_REMOVAL', True)
        self.auto_crop = getattr(settings, 'AUTO_CROP', True)
        
        # Initialize face detection
        try:
            # Load OpenCV's face detection classifier
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.face_detection_available = True
        except Exception as e:
            logger.warning(f"Face detection not available: {e}")
            self.face_detection_available = False
    
    def process_avatar(self, image_file) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Main processing pipeline for avatar creation
        
        Args:
            image_file: Uploaded image file
            
        Returns:
            Tuple of (processed_image, processing_metadata)
        """
        processing_info = {
            'cropped': False,
            'background_removed': False,
            'face_detected': False,
            'enhanced': False,
            'original_size': None,
            'final_size': None
        }
        
        try:
            # Load and prepare image
            image = self._load_image(image_file)
            processing_info['original_size'] = image.size
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA'):
                # Keep alpha channel for transparency
                pass
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Step 1: Face detection and smart cropping
            if self.auto_crop and self.face_detection_available:
                cropped_image, face_found = self._smart_crop_face(image)
                if face_found:
                    image = cropped_image
                    processing_info['cropped'] = True
                    processing_info['face_detected'] = True
                else:
                    # Fallback to center crop
                    image = self._center_crop_square(image)
                    processing_info['cropped'] = True
            else:
                # Center crop if no face detection
                image = self._center_crop_square(image)
                processing_info['cropped'] = True
            
            # Step 2: Enhance image quality
            image = self._enhance_image(image)
            processing_info['enhanced'] = True
            
            # Step 3: Background removal
            if self.background_removal:
                image = self._remove_background(image)
                processing_info['background_removed'] = True
            
            # Step 4: Resize to target size
            image = self._resize_image(image, (self.output_size, self.output_size))
            processing_info['final_size'] = image.size
            
            # Step 5: Final optimization
            image = self._optimize_avatar(image)
            
            return image, processing_info
            
        except Exception as e:
            logger.error(f"Error processing avatar: {e}")
            raise
    
    def _load_image(self, image_file) -> Image.Image:
        """Load and validate image file"""
        try:
            image = Image.open(image_file)
            # Verify it's a valid image
            image.verify()
            # Reload for processing (verify() closes the file)
            image_file.seek(0)
            image = Image.open(image_file)
            return image
        except Exception as e:
            raise ValueError(f"Invalid image file: {e}")
    
    def _smart_crop_face(self, image: Image.Image) -> Tuple[Image.Image, bool]:
        """
        Detect face and crop around it for better portrait composition
        
        Returns:
            Tuple of (cropped_image, face_detected)
        """
        try:
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces with multiple scale factors for better detection
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,  # More sensitive detection
                minNeighbors=3,    # Less strict neighbor requirement
                minSize=(20, 20),  # Smaller minimum size
                maxSize=(int(gray.shape[0]*0.8), int(gray.shape[1]*0.8)),  # Maximum size
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # If no faces found with strict parameters, try more relaxed detection
            if len(faces) == 0:
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=2,
                    minSize=(15, 15),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
            
            if len(faces) > 0:
                # Use the largest face
                largest_face = max(faces, key=lambda face: face[2] * face[3])
                x, y, w, h = largest_face
                
                # Calculate crop area with padding for better portrait
                padding_factor = 1.2  # Add 120% padding around face for better portrait
                center_x, center_y = x + w // 2, y + h // 2
                
                # Calculate crop size (make it square) - include more area for hair
                face_size = max(w, h)
                crop_size = int(face_size * (1 + padding_factor))
                
                # Adjust center point slightly upward to include more hair
                center_y = max(center_y - int(h * 0.1), center_y)
                
                # Ensure crop area is within image bounds with safety margins
                img_width, img_height = image.size
                half_crop = crop_size // 2
                
                # Calculate initial crop bounds
                left = max(0, center_x - half_crop)
                top = max(0, center_y - half_crop)
                right = min(img_width, center_x + half_crop)
                bottom = min(img_height, center_y + half_crop)
                
                # Safety check: ensure we have a reasonable crop size
                crop_width = right - left
                crop_height = bottom - top
                min_crop_size = min(img_width, img_height) * 0.3  # At least 30% of image
                
                if crop_width < min_crop_size or crop_height < min_crop_size:
                    # Fall back to center crop if face detection resulted in too small area
                    return self._center_crop_square(image), False
                
                # Adjust to maintain square aspect ratio
                crop_width = right - left
                crop_height = bottom - top
                
                if crop_width < crop_height:
                    # Adjust width
                    diff = crop_height - crop_width
                    left = max(0, left - diff // 2)
                    right = min(img_width, left + crop_height)
                elif crop_height < crop_width:
                    # Adjust height
                    diff = crop_width - crop_height
                    top = max(0, top - diff // 2)
                    bottom = min(img_height, top + crop_width)
                
                cropped = image.crop((left, top, right, bottom))
                return cropped, True
            
            return image, False
            
        except Exception as e:
            logger.warning(f"Face detection failed: {e}")
            return image, False
    
    def _center_crop_square(self, image: Image.Image) -> Image.Image:
        """Crop image to square from center with portrait optimization"""
        width, height = image.size
        
        # For portrait optimization, prefer to keep more of the top area
        if height > width:
            # Portrait orientation - crop from bottom more than top
            size = width
            left = 0
            # Keep more area from top (where face/hair usually is)
            top = max(0, int(height * 0.1))  # Start 10% from top
            right = width
            bottom = min(height, top + size)
            
            # Adjust if we don't have enough space
            if bottom - top < size:
                top = max(0, height - size)
                bottom = height
                
        else:
            # Landscape or square - center crop
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
        
        return image.crop((left, top, right, bottom))
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """Enhance image quality with portrait-specific adjustments"""
        try:
            # Gentle sharpening for portraits
            image = image.filter(ImageFilter.UnsharpMask(radius=0.8, percent=110, threshold=3))
            
            # Slightly enhance contrast for definition
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.08)
            
            # Gentle color enhancement
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.03)
            
            # Slight brightness adjustment for portraits
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.02)
            
            return image
            
        except Exception as e:
            logger.warning(f"Image enhancement failed: {e}")
            return image
    
    def _remove_background(self, image: Image.Image) -> Image.Image:
        """Remove background and make it transparent"""
        try:
            # Convert to bytes for rembg
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Remove background
            result = remove(img_byte_arr)
            
            # Convert back to PIL Image
            processed_image = Image.open(io.BytesIO(result))
            
            # Ensure RGBA mode for transparency
            if processed_image.mode != 'RGBA':
                processed_image = processed_image.convert('RGBA')
            
            return processed_image
            
        except Exception as e:
            logger.error(f"Background removal failed: {e}")
            # Return original image if background removal fails
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            return image
    
    def _resize_image(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """Resize image with high quality resampling"""
        return image.resize(size, Image.Resampling.LANCZOS)
    
    def _optimize_avatar(self, image: Image.Image) -> Image.Image:
        """Final optimization for avatar image"""
        try:
            # Ensure RGBA mode for transparency
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Apply slight blur to alpha channel for smoother edges
            alpha = image.split()[-1]
            alpha = alpha.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # Reconstruct image with smoothed alpha
            if len(image.split()) == 4:
                r, g, b, _ = image.split()
                image = Image.merge('RGBA', (r, g, b, alpha))
            
            return image
            
        except Exception as e:
            logger.warning(f"Final optimization failed: {e}")
            return image
    
    def save_processed_image(self, image: Image.Image, output_path: str) -> int:
        """
        Save processed image with optimization
        
        Returns:
            File size in bytes
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save with optimization
            image.save(
                output_path,
                format='PNG',
                optimize=True,
                compress_level=6  # Good compression without quality loss
            )
            
            return os.path.getsize(output_path)
            
        except Exception as e:
            logger.error(f"Failed to save processed image: {e}")
            raise


class ImageValidator:
    """Utility class for image validation"""
    
    @staticmethod
    def validate_image_file(image_file) -> Dict[str, Any]:
        """
        Validate uploaded image file
        
        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'info': {}
        }
        
        try:
            # Check file size
            file_size = image_file.size
            max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10485760)
            
            if file_size > max_size:
                result['errors'].append(f"File too large: {file_size} bytes (max: {max_size})")
                return result
            
            result['info']['file_size'] = file_size
            
            # Check image validity
            image = Image.open(image_file)
            image.verify()
            
            # Reset file pointer
            image_file.seek(0)
            image = Image.open(image_file)
            
            result['info']['format'] = image.format
            result['info']['mode'] = image.mode
            result['info']['size'] = image.size
            
            # Check minimum dimensions
            width, height = image.size
            if width < 100 or height < 100:
                result['warnings'].append("Image is quite small, quality may be affected")
            
            # Check aspect ratio
            aspect_ratio = width / height
            if aspect_ratio > 2 or aspect_ratio < 0.5:
                result['warnings'].append("Unusual aspect ratio detected")
            
            result['valid'] = True
            
        except Exception as e:
            result['errors'].append(f"Invalid image file: {str(e)}")
        
        return result
