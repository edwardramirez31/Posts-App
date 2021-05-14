from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Notification
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.
def get_notifications(request):
    search_value = request.GET.get('search', False)
    if search_value:
        query = Q(sender__username__icontains=search_value)
        notifications = Notification.objects.filter(query).select_related().order_by('-date')
    else:
        notifications = request.user.get_all_notifications.all().order_by('-date')
        
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context = {'page_obj': page_obj}
    return render(request, 'notifications/list.html', context)


def mark_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.has_seen = True
    notification.save()
    return redirect(notification.get_url())

def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, )
    try:
        notification.delete()
        message = "Success"
    except:
        message = "Something went wrong"

    return HttpResponse(message)