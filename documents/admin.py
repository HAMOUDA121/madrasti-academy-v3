from django.contrib import admin
from .models import Document, DocumentChunk

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'subject', 'uploaded_at')

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'chunk_index')
