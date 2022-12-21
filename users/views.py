import collections
import json
from typing import List, Dict

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location


class UserListView(ListView):
    """
    Отображает таблицу User
    """
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list.order_by("username"), 2)
        start_page = request.GET.get("page", 1)
        paginator_object = paginator.get_page(start_page)

        users: collections.Iterable = paginator_object
        response_as_list: List[Dict[str, int | str]] = []
        for user in users:
            response_as_list.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "age": user.age,
                    "locations": [
                        _location.name for _location in user.location.all()
                    ]
                }
            )

        result_dict = {
            "items": response_as_list,
            "pages number": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(result_dict, safe=False,
                            json_dumps_params={"ensure_ascii": False, "indent": 4})


