from django.shortcuts import render, redirect
from django.conf import settings
from .models import PDFDocument
from llama_index import SimpleDirectoryReader
from llama_index import GPTVectorStoreIndex
import openai
from llama_index import StorageContext, load_index_from_storage
openai.api_key = settings.OPENAI_API_KEY


def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        document = PDFDocument(name=pdf_file.name, pdf_file=pdf_file)
        document.save()
        # ファイルの保存に成功した場合の処理を追加
        return redirect('confirm_upload')
    return render(request, 'upload_pdf.html')

def confirm_upload(request):
    return render(request, 'confirm_upload.html')

def dealing_pdf(request):
    # ファイルの読み込み処理を書く
    documents = SimpleDirectoryReader("pdfs").load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    return redirect('ask_questions')

def ask_questions(request):
    if request.method == 'POST':
        question = request.POST['question']
        # ここで質問に対する回答を取得する処理を書く
        strorage_context = StorageContext.from_defaults(persist_dir='./storage')
        index = load_index_from_storage(strorage_context)
        query_engine = index.as_query_engine()
        answer = query_engine.query(question)
        return render(request, 'answer.html', {'answer':answer})
    else:
        return render(request, 'ask.html',)

