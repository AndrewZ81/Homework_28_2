import collections
import json
from typing import List, Dict

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from advertisements.models import Category, Advertisement


def show_main_page(request) -> JsonResponse:
    return JsonResponse({"status": "ok"}, status=200)


class CategoryListView(ListView):
    """
    Отображает таблицу Category
    """
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        super().get(request, *args, **kwargs)
        categories: collections.Iterable = self.object_list.order_by("name")
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


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    """
    Cоздаёт новую запись Category
    """
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs) -> JsonResponse:
        category_data: Dict[str, str] = json.loads(request.body)
        category: Category = Category.objects.create(**category_data)
        response_as_dict: Dict[str, int | str] = {
            "id": category.id,
            "name": category.name
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    """
    Редактирует запись Category
    """
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        super().post(request, *args, **kwargs)
        category_data: Dict[str, str] = json.loads(request.body)

        if "name" in category_data:
            self.object.name = category_data["name"]
        self.object.save()

        response_as_dict: Dict[str, int | str] = {
            "id": self.object.id,
            "name": self.object.name
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    """
    Удаляет запись Category
    """
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


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


class AdvertisementListView(ListView):
    """
    Отображает таблицу Advertisement
    """
    model = Advertisement

    def get(self, request, *args, **kwargs) -> JsonResponse:
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list.order_by("-price"), 5)
        start_page = request.GET.get("page", 1)
        paginator_object = paginator.get_page(start_page)

        advertisements: collections.Iterable = paginator_object
        response_as_list: List[Dict[str, int | str]] = []
        for advertisement in advertisements:
            response_as_list.append(
                {
                    "id": advertisement.id,
                    "name": advertisement.name,
                    "author": advertisement.author_id,
                    "price": advertisement.price,
                }
            )

        result_dict = {
            "items": response_as_list,
            "pages nuber": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(result_dict, safe=False,
                            json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementCreateView(CreateView):
    """
    Cоздаёт новую запись Advertisement
    """
    model = Advertisement
    fields = "__all__"

    def post(self, request, *args, **kwargs) -> JsonResponse:
        advertisement_data: Dict[str, int | str] = json.loads(request.body)
        advertisement: Advertisement = Advertisement.objects.create(**advertisement_data)
        response_as_dict: Dict[str, int | str] = {
            "id": advertisement.id,
            "name": advertisement.name,
            "author_id": advertisement.author.id,
            "author": advertisement.author.username,
            "price": advertisement.price,
            "description": advertisement.description,
            "address": [
                _location.name for _location in advertisement.author.location.all()
            ],
            "image": advertisement.image.url if advertisement.image else None,
            "is_published": advertisement.is_published,
            "category_id": advertisement.category.id,
            "category_name": advertisement.category.name,
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})


class AdvertisementDetailView(DetailView):
    """
    Делает выборку записи из таблицы Advertisement по id
    """
    model = Advertisement

    def get(self, request, *args, **kwargs) -> JsonResponse:
        advertisement: Advertisement = self.get_object()
        response: Dict[str, int | str] = {
            "id": advertisement.id,
            "name": advertisement.name,
            "author_id": advertisement.author_id,
            "author": advertisement.author.username,
            "price": advertisement.price,
            "description": advertisement.description,
            "address": [
                _location.name for _location in advertisement.author.location.all()
            ],
            "image": advertisement.image.url if advertisement.image else None,
            "is_published": advertisement.is_published,
            "category_id": advertisement.category.id,
            "category_name": advertisement.category.name,
        }
        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementUpdateView(UpdateView):
    """
    Редактирует запись Advertisement
    """
    model = Advertisement
    fields = "__all__"

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        super().post(request, *args, **kwargs)
        advertisement_data: Dict[str, str | int] = json.loads(request.body)

        if "name" in advertisement_data:
            self.object.name = advertisement_data["name"]
        if "author_id" in advertisement_data:
            self.object.author_id = advertisement_data["author_id"]
        if "price" in advertisement_data:
            self.object.price = advertisement_data["price"]
        if "description" in advertisement_data:
            self.object.description = advertisement_data["description"]
        if "category_id" in advertisement_data:
            self.object.category_id = advertisement_data["category_id"]

        self.object.save()

        response_as_dict: Dict[str, int | str] = {
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "address": [
                _location.name for _location in self.object.author.location.all()
            ],
            "image": self.image.url if self.image else None,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "category_name": self.object.category.name,
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementDeleteView(DeleteView):
    """
    Удаляет запись Advertisement
    """
    model = Advertisement
    success_url = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementUploadImage(UpdateView):
    """
    Добавляет изображение к записи Advertisement по id
    """
    model = Advertisement
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object: Advertisement = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        response_as_dict: Dict[str, int | str] = {
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "address": [
                _location.name for _location in self.object.author.location.all()
            ],
            "image": self.object.image.url,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "category_name": self.object.category.name,
        }
        return JsonResponse(response_as_dict, json_dumps_params={"ensure_ascii": False, "indent": 4})
