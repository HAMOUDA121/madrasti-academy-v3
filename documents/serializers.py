from rest_framework import serializers
from .models import Document, DocumentChunk

class DocumentSerializer(serializers.ModelSerializer):
    grade_display = serializers.CharField(source='get_grade_display', read_only=False)

    class Meta:
        model = Document
        fields = ['id', 'title', 'grade', 'grade_display', 'subject', 'file', 'uploaded_at']
