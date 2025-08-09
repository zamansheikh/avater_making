"""
Professional Avatar Processing API Views

This module provides REST API endpoints for avatar image processing with:
- Secure file upload handling
- Comprehensive error handling
- Professional response formatting
- Detailed logging and monitoring
"""

import logging
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image
import io

from .models import ProcessedAvatar
from .serializers import (
    AvatarUploadSerializer,
    ProcessedAvatarSerializer,
    AvatarProcessResponseSerializer
)
from .services import AvatarProcessor, ImageValidator

logger = logging.getLogger(__name__)


class AvatarProcessAPIView(APIView):
    """
    Professional API endpoint for avatar image processing
    
    POST /api/process-avatar/
    - Accepts image upload
    - Processes image with AI-powered enhancements
    - Returns processed avatar URL with metadata
    """
    
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        """Process uploaded image and create avatar"""
        
        # Log request details
        user_ip = self._get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        logger.info(f"Avatar processing request from {user_ip}")
        
        try:
            # Validate input
            serializer = AvatarUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return self._error_response(
                    "Invalid input data",
                    serializer.errors,
                    status.HTTP_400_BAD_REQUEST
                )
            
            image_file = serializer.validated_data['image']
            original_filename = image_file.name
            
            # Additional image validation
            validation_result = ImageValidator.validate_image_file(image_file)
            if not validation_result['valid']:
                return self._error_response(
                    "Image validation failed",
                    validation_result['errors'],
                    status.HTTP_400_BAD_REQUEST
                )
            
            # Create database record
            avatar_record = ProcessedAvatar.objects.create(
                original_image=image_file,
                original_filename=original_filename,
                processing_status='processing',
                file_size_original=image_file.size,
                user_ip=user_ip,
                user_agent=user_agent
            )
            
            try:
                # Process the image
                processor = AvatarProcessor()
                
                # Reset file pointer before processing
                image_file.seek(0)
                processed_image, processing_info = processor.process_avatar(image_file)
                
                # Save processed image
                processed_filename = f"avatar_{avatar_record.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.png"
                
                # Convert PIL image to file
                img_buffer = io.BytesIO()
                processed_image.save(img_buffer, format='PNG', optimize=True)
                img_buffer.seek(0)
                
                # Save to model
                avatar_record.processed_image.save(
                    processed_filename,
                    ContentFile(img_buffer.getvalue()),
                    save=False
                )
                
                # Update processing metadata
                avatar_record.processing_status = 'completed'
                avatar_record.was_cropped = processing_info.get('cropped', False)
                avatar_record.background_removed = processing_info.get('background_removed', False)
                avatar_record.output_width = processed_image.size[0]
                avatar_record.output_height = processed_image.size[1]
                avatar_record.file_size_processed = len(img_buffer.getvalue())
                avatar_record.save()
                
                # Prepare response
                avatar_serializer = ProcessedAvatarSerializer(
                    avatar_record,
                    context={'request': request}
                )
                
                response_data = {
                    'success': True,
                    'message': 'Avatar processed successfully',
                    'processed_image_url': avatar_serializer.data['processed_image_url'],
                    'original_filename': original_filename,
                    'processing_details': avatar_record.processing_details,
                    'avatar_id': avatar_record.id
                }
                
                # Add warnings if any
                if validation_result['warnings']:
                    response_data['warnings'] = validation_result['warnings']
                
                logger.info(f"Avatar {avatar_record.id} processed successfully")
                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except Exception as processing_error:
                # Update record with error
                avatar_record.processing_status = 'failed'
                avatar_record.error_message = str(processing_error)
                avatar_record.save()
                
                logger.error(f"Processing failed for avatar {avatar_record.id}: {processing_error}")
                return self._error_response(
                    "Image processing failed",
                    str(processing_error),
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            logger.error(f"Unexpected error in avatar processing: {e}")
            return self._error_response(
                "Server error occurred",
                "Please try again later",
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _error_response(self, message, error_details, status_code):
        """Create standardized error response"""
        return Response({
            'success': False,
            'message': message,
            'error': error_details
        }, status=status_code)


@api_view(['GET'])
def avatar_status(request, avatar_id):
    """
    Get processing status of an avatar
    
    GET /api/avatar-status/{avatar_id}/
    """
    try:
        avatar = ProcessedAvatar.objects.get(id=avatar_id)
        serializer = ProcessedAvatarSerializer(avatar, context={'request': request})
        
        return Response({
            'success': True,
            'avatar': serializer.data
        })
        
    except ProcessedAvatar.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Avatar not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint for monitoring
    
    GET /api/health/
    """
    try:
        # Basic health checks
        health_data = {
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'services': {
                'database': 'healthy',
                'image_processing': 'healthy',
                'file_storage': 'healthy'
            }
        }
        
        # Check database
        try:
            ProcessedAvatar.objects.first()
        except Exception as e:
            health_data['services']['database'] = f'error: {e}'
            health_data['status'] = 'degraded'
        
        # Check image processing
        try:
            processor = AvatarProcessor()
            if not processor.face_detection_available:
                health_data['services']['image_processing'] = 'warning: face detection unavailable'
        except Exception as e:
            health_data['services']['image_processing'] = f'error: {e}'
            health_data['status'] = 'degraded'
        
        # Check file storage
        try:
            media_root = settings.MEDIA_ROOT
            if not os.path.exists(media_root):
                os.makedirs(media_root)
        except Exception as e:
            health_data['services']['file_storage'] = f'error: {e}'
            health_data['status'] = 'degraded'
        
        return Response(health_data)
        
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def api_info(request):
    """
    API information and documentation
    
    GET /api/info/
    """
    return Response({
        'name': 'Avatar Processing API',
        'version': '1.0.0',
        'description': 'Professional avatar creation from uploaded images',
        'endpoints': {
            '/api/process-avatar/': {
                'method': 'POST',
                'description': 'Upload and process image to create avatar',
                'content_type': 'multipart/form-data',
                'parameters': {
                    'image': 'Image file (JPG, PNG, WEBP)'
                },
                'max_file_size': f"{settings.MAX_UPLOAD_SIZE // (1024*1024)}MB"
            },
            '/api/avatar-status/{id}/': {
                'method': 'GET',
                'description': 'Get processing status of an avatar'
            },
            '/api/health/': {
                'method': 'GET',
                'description': 'Health check endpoint'
            },
            '/api/info/': {
                'method': 'GET',
                'description': 'API information and documentation'
            }
        },
        'features': [
            'AI-powered face detection and cropping',
            'Automatic background removal',
            'Image enhancement and optimization',
            'Transparent PNG output',
            'Professional error handling',
            'Processing status tracking'
        ],
        'settings': {
            'output_size': f"{settings.OUTPUT_IMAGE_SIZE}x{settings.OUTPUT_IMAGE_SIZE}",
            'background_removal': settings.BACKGROUND_REMOVAL,
            'auto_crop': settings.AUTO_CROP,
            'allowed_formats': settings.ALLOWED_IMAGE_TYPES
        }
    })
