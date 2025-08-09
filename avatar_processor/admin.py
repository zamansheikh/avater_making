from django.contrib import admin
from .models import ProcessedAvatar


@admin.register(ProcessedAvatar)
class ProcessedAvatarAdmin(admin.ModelAdmin):
    """Admin interface for ProcessedAvatar model"""
    
    list_display = [
        'id',
        'original_filename',
        'processing_status',
        'was_cropped',
        'background_removed',
        'output_dimensions',
        'created_at'
    ]
    
    list_filter = [
        'processing_status',
        'was_cropped',
        'background_removed',
        'created_at'
    ]
    
    search_fields = [
        'original_filename',
        'user_ip'
    ]
    
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'file_size_original',
        'file_size_processed',
        'processing_details'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'original_filename', 'processing_status')
        }),
        ('Images', {
            'fields': ('original_image', 'processed_image')
        }),
        ('Processing Details', {
            'fields': (
                'was_cropped',
                'background_removed',
                'output_width',
                'output_height',
                'file_size_original',
                'file_size_processed'
            )
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('User Information', {
            'fields': ('user_ip', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def output_dimensions(self, obj):
        """Display output dimensions"""
        if obj.output_width and obj.output_height:
            return f"{obj.output_width}x{obj.output_height}"
        return "N/A"
    
    output_dimensions.short_description = "Output Size"
    
    def has_delete_permission(self, request, obj=None):
        """Restrict deletion for completed avatars"""
        if obj and obj.processing_status == 'completed':
            return request.user.is_superuser
        return True
