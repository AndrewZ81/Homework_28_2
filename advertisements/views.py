import collections
import json
from typing import List, Dict

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from advertisements.models import Category


def show_main_page(request) -> JsonResponse:
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):
    """
    Отображает таблицу Category или создаёт новую запись Category
    """
    def get(self, request) -> JsonResponse:
        categories: collections.Iterable = Category.objects.all()
        response_as_list: List[Dict[str, int | str]] = []
        for category in categories:
            response_as_list.append(
                {
                    "id": category.id,
                    "name": category.name
                }
            )
        return JsonResponse(response_as_list, safe=False,
                            json_dumps_params={"ensure_ascii": False, "indent": 4})

    def post(self, request) -> JsonResponse:
        category_data: Dict[str, int | str] = json.loads(request.body)
        category: Category = Category(**category_data)
        category.save()
        response_as_dict: Dict[str, int | str] = {
            "id": category.id,
            "name": category.name
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})


class CategoryDetailView(DetailView):
    """
    Делает выборку записи из таблицы Category по id
    """
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        category: Category = self.get_object()
        response: Dict[str, int | str] = {
            "id": category.id,
            "name": category.name
        }
        return JsonResponse(response, json_dumps_params={"ensure_ascii": False, "indent": 4})
