from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from main.forms import imageFeedForm, imageAttForm
from main.funcs import recognize_image, attendance_image

# Create your views here.
@login_required
def attendanceView(request):
    return render(request, 'attendance.html', {})

@login_required
def surveillance(request):
    return render(request, 'surveillance.html', {})

def getImageForAttendance(request):
    if request.method == 'POST':
        # print(request.POST)
        form = imageAttForm(data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data.get('image'))
            detection = attendance_image(form.cleaned_data.get('image'),form.cleaned_data.get('batch'),form.cleaned_data.get('section') )
            # while(True):
            #     cv2.imshow('frame',cvimg)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
            # cv2.destroyAllWindows()
            return HttpResponse(detection)
        else:
            print(form.errors)
            return HttpResponse('invalid form')


def getImagefromFeed(request):
    if request.method == 'POST':
        # print(request.POST)
        form = imageFeedForm(data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data.get('image'))
            detection = recognize_image(form.cleaned_data.get('image'))
            # while(True):
            #     cv2.imshow('frame',cvimg)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
            # cv2.destroyAllWindows()
            if detection:
                return HttpResponse(detection)
            else:
                return HttpResponse('false')
        else:
            print(form.errors)
            return HttpResponse('invalid form')