from django.db import models
from django.core.validators import FileExtensionValidator
import uuid
import os


def upload_to_original(instance, filename):
    """Generate upload path for original images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/original', filename)


def upload_to_processed(instance, filename):
    """Generate upload path for processed images"""
    ext = filename.split('.')[-1]
    filename = f"avatar_{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/processed', filename)


class ProcessedAvatar(models.Model):
    """Model to store avatar processing information"""
    
    # Original image details
    original_image = models.ImageField(
        upload_to=upload_to_original,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Original uploaded image"
    )
    original_filename = models.CharField(max_length=255, help_text="Original filename")
    
    # Processed image details
    processed_image = models.ImageField(
        upload_to=upload_to_processed,
        blank=True,
        null=True,
        help_text="Processed avatar image"
    )
    
    # Processing metadata
    processing_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    
    # Processing details
    was_cropped = models.BooleanField(default=False)
    background_removed = models.BooleanField(default=False)
    output_width = models.PositiveIntegerField(null=True, blank=True)
    output_height = models.PositiveIntegerField(null=True, blank=True)
    file_size_original = models.PositiveIntegerField(null=True, blank=True, help_text="Size in bytes")
    file_size_processed = models.PositiveIntegerField(null=True, blank=True, help_text="Size in bytes")
    
    # Error information
    error_message = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional: User tracking (if you want to track uploads by user)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Processed Avatar"
        verbose_name_plural = "Processed Avatars"
    
    def __str__(self):
        return f"Avatar {self.id} - {self.processing_status}"
    
    @property
    def processing_details(self):
        """Return processing details as dictionary"""
        return {
            'cropped': self.was_cropped,
            'background_removed': self.background_removed,
            'size': f"{self.output_width}x{self.output_height}" if self.output_width and self.output_height else None,
            'original_size_bytes': self.file_size_original,
            'processed_size_bytes': self.file_size_processed,
        }
