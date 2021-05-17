from django import template

register = template.Library()

# {% load user_info %}
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


# {{somevariable | cut: "0"}}
register.filter('cut', cut)

def display_info(user, current_user):
    print(user, current_user)
    followers = set([profile.user for profile in user.all_followers.all()])
    print(followers)
    following = set(current_user.profile.following.all())
    print(following)
    intersection = list(followers.intersection(following))

    if len(intersection) > 1:
        return f"{intersection[0]} and {len(intersection) - 1} more follow this account"
    elif len(intersection) == 1:
        return f"{intersection[0]} follows this account"

    elif user.profile in current_user.all_followers.all():
        return "Follows you"
    else:
        return "Suggestion for you"


register.filter('display_info', display_info)

@register.inclusion_tag("blog/notifications.html", takes_context=True)
def show_notifications(context):
    user = context['request'].user
    notifications = user.get_all_notifications.all().order_by('-date')
    not_seen = len(notifications.filter(has_seen=False))
    return {"notifications": notifications[:7], "not_seen": not_seen}


# se hace debido a que no hay logica para una vista de solo la navbar
