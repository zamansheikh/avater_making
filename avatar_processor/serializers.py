from rest_framework import serializers
from .models import ProcessedAvatar


class AvatarUploadSerializer(serializers.Serializer):
    """Serializer for avatar image upload"""
    
    image = serializers.ImageField(
        required=True,
        help_text="Image file to process (JPG, PNG, WEBP supported)"
    )
    
    def validate_image(self, value):
        """Validate uploaded image"""
        from django.conf import settings
        
        # Check file size
        if value.size > settings.MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(
                f"File size too large. Maximum size is {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB"
            )
        
        # Check file extension
        ext = value.name.split('.')[-1].lower()
        if ext not in settings.ALLOWED_IMAGE_TYPES:
            raise serializers.ValidationError(
                f"Unsupported file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
            )
        
        return value


class ProcessedAvatarSerializer(serializers.ModelSerializer):
    """Serializer for processed avatar response"""
    
    processed_image_url = serializers.SerializerMethodField()
    processing_details = serializers.ReadOnlyField()
    
    class Meta:
        model = ProcessedAvatar
        fields = [
            'id',
            'original_filename',
            'processed_image_url',
            'processing_status',
            'processing_details',
            'created_at',
            'error_message'
        ]
    
    def get_processed_image_url(self, obj):
        """Get the full URL for the processed image"""
        if obj.processed_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.processed_image.url)
            return obj.processed_image.url
        return None


class AvatarProcessResponseSerializer(serializers.Serializer):
    """Serializer for API response"""
    
    success = serializers.BooleanField()
    message = serializers.CharField(required=False)
    processed_image_url = serializers.URLField(required=False)
    original_filename = serializers.CharField(required=False)
    processing_details = serializers.DictField(required=False)
    avatar_id = serializers.IntegerField(required=False)
    error = serializers.CharField(required=False)
