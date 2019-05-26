from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from main.forms import imageFeedForm
import cv2, threading, base64
from PIL import Image
from io import StringIO, BytesIO
import numpy as np

def readb64(base64_string):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)


# Create your views here.
@login_required
def attendanceView(request):
    return render(request, 'attendance.html', {});


def getImagefromFeed(request):
    if request.method == 'POST':
        # print(request.POST)
        form = imageFeedForm(data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data.get('image'))
            cvimg = readb64(form.cleaned_data.get('image'))
            while(True):
                cv2.imshow('frame',cvimg)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()
            return HttpResponse('success')
        else:
            print(form.errors)
            return HttpResponse('invalid form')