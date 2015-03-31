from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Article

@transaction.non_atomic_requests # 以下http request不被包裹在一个transaction中
def posting_flavor_status(request, pk, title):
    flavor = get_object_or_404(Article, pk=pk)

        # 以下代码会以django默认的autocommit模式执行
    flavor.datetime = timezone.now()
    flavor.save()

    with transaction.atomic():
            # 以下代码被包裹在另一个transaction中
        flavor.title = title
        flavor.datetime = timezone.now()
        flavor.save()
        return HttpResponse("Hooray")

        # 如果以上transaction失败了, 返回错误状态
    return HttpResponse("Sadness", status_code=400)