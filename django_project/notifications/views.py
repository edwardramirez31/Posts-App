from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Notification
# Create your views here.
def get_notifications(request):
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