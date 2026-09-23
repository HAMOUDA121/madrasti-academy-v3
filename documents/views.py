import pypdf
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Document, DocumentChunk
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UploadDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        title = request.data.get('title')
        grade = request.data.get('grade', 'BAC_MATH')
        subject = request.data.get('subject', 'عام')
        file_obj = request.FILES.get('file')

        if not title or not file_obj:
            return Response({'error': 'يرجى تقديم العنوان والملف'}, status=status.HTTP_400_BAD_REQUEST)

        doc = Document.objects.create(
            title=title,
            grade=grade,
            subject=subject,
            file=file_obj
        )

        # استخراج النصوص وتقسيمها إلى Chunks لتقنية RAG
        try:
            reader = pypdf.PdfReader(doc.file.path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            # تقسيم النص إلى فقرات بحجم ~600 حرف
            chunk_size = 600
            chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
            
            for idx, c in enumerate(chunks):
                if c.strip():
                    DocumentChunk.objects.create(
                        document=doc,
                        content=c.strip(),
                        chunk_index=idx
                    )

            return Response({
                'message': f'تم رفع الوثيقة بنجاح وتم توليد {len(chunks)} جزءاً للمواضيع والمناهج!',
                'document': DocumentSerializer(doc).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'فشل استخراج النص من PDF: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
