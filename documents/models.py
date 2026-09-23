from django.db import models

class Document(models.Model):
    GRADE_CHOICES = [
        ('BAC_MATH', 'باكالوريا رياضيات'),
        ('BAC_INFO', 'باكالوريا علوم الإعلامية'),
        ('BAC_SC', 'باكالوريا علوم تجريبية'),
        ('9TH_GRADE', 'التاسعة أساسي (نوفيام)'),
    ]
    title = models.CharField(max_length=200)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default='BAC_MATH')
    subject = models.CharField(max_length=100, default='عام')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_grade_display()})"

class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    chunk_index = models.IntegerField()

    def __str__(self):
        return f"{self.document.title} - جزء {self.chunk_index}"
