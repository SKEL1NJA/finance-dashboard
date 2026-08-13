import json

from django.shortcuts import render

from .dashboard_services import get_category_breakdown, get_monthly_trend, get_net_worth


def dashboard_view(request):
    context = {
        'net_worth': get_net_worth(request.user),
        'monthly_trend': json.dumps(get_monthly_trend(request.user)),
        'category_breakdown': json.dumps(get_category_breakdown(request.user)),
    }
    return render(request, 'dashboard.html', context)