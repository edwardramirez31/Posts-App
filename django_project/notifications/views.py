from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
def get_notifications(request):
    notifications = request.user.get_all_notifications.all().order_by('-date')
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context = {'page_obj': page_obj}
    return render(request, 'notifications/list.html', context)
