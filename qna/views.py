from dataclasses import dataclass
from distutils.command.upload import upload
import os
from xmlrpc.client import ResponseError
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.conf import settings
from MyHome import board
from MyHome.board.models import Board
from ddm.models import AdminMember, Qna,Member,QnaFile
from datetime import datetime
import os
from django.shortcuts import render,redirect,Response,ObjectDoesNotExist
from django.http import HttpRequest
from django.conf import settings


def fileForm(request):
    return render(request,'Question.html')

def fileUpload(request:HttpRequest):
    qa_kind_idx = request.POST.get('qa_kind_idx')
    #파일같은경우는 FILES로 전달된다..
    content = request.POST.get('content') 
    # status = request.POST.get('status')
    
    
    dt=datetime.now()


    mem = Member.objects.filter(mem_idx = 1) 
    mem1= mem[0]
    admin_test = AdminMember.objects.filter(idx = 1) 
    admin_test1=admin_test[0]

    fileModel = Qna.objects.create(qa_kind_idx=qa_kind_idx,member_idx=mem1,content=content,
    datetime=dt,status=0,admin_idx= admin_test1)
    files = request.FILES.getlist('files')

    print(files)
    for file in files:
        print(file)
        uf = QnaFile(qna_idx=fileModel,upload_route=file,filename=file.name,size=file.size)
        uf.save()

    print(dt)


    print(fileModel)
    context = {
        'f' : fileModel,
    }


    return render(request,'index.html',context)

# @login_message_required

def fileChange(request:HttpRequest):
    mem = Member.objects.get(mem_idx=1)
    qna = Qna.objects.get(q_idx = 12)
    qa_kind_idx = request.POST.get('qa_kind_idx')
    #파일같은경우는 FILES로 전달된다..
    content = request.POST.get('content') 
    get_files = request.FILES.getlist('files')

    # notice = Qna.objects.filter(q_idx = q_idx) 
    # notice = Member.objects.get(mem_idx = 1)
    
    try:
        notice = Qna.objects.get(qa_kind_idx = qna) 
        if qa_kind_idx != 0:
            notice.qa_kind_idx = qa_kind_idx
        if content != "":
            notice.content = content
        if files != "":
                    
            notice.files = files

        try:
            notice.save()
            return redirect('/notice')
        except ValueError:
            return Response({"success":False,"msg":"에러입니다."})
    except ObjectDoesNotExist:
         return Response({"success":False,"msg":"게시글 없음."})




# def fileDelete(request):
#     files = QnaFile.objects.filter(upload=5)

#     for file in files:
#         print(file.upload_file.url)
#         path = os.path.dirname(file.upload_file.name)
#         file.delete()

#     #print(os.path.join(settings.MEDIA_ROOT,path))
#     #print(os.path.exists(os.path.join(settings.MEDIA_ROOT,path)))
#     if os.path.exists(os.path.join(settings.MEDIA_ROOT,path)): # 해당 경로에 폴더가 있으면..
#         try:
#             os.rmdir(os.path.join(settings.MEDIA_ROOT,path))
#             # rmdir - 비어있는 폴더 삭제
#             # rmtree - 폴더와 그 안에 있는 파일 모두 삭제
#         except:
#             pass
        
#     return redirect('/')

# @receiver(post_delete,sender=QnaFile)
# def deleteFile(sender,**kwargs):
#     print('deleteFile')
#     files = kwargs.get('instance') 
#     files.upload_file.delete(save=False)