from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotAuthenticated, PermissionDenied

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from requests import get
from yaml import load as load_yaml, Loader

from app.models import Shop, Category, ProductInfo, Product, Parameter, ProductParameter

# class PartnerUpdate(APIView):
#     """
#     Класс для обновления прайса от поставщика
#     """
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             # return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
#             return NotAuthenticated
#         if request.user.type != 'shop':
#             # return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)
#             return PermissionDenied
#         # #TODO обернуть try/except GET-запрос  
#         url = request.data.get('url')
#         if url:
#             validate_url = URLValidator()
#             try:
#                 validate_url(url)
#             except ValidationError as e:
#                 # return JsonResponse({'Status': False, 'Error': str(e)})
#                 raise APIException(detail={'Status': False, 'Error': str(e)})
#             else:
#                 # stream = get(url).content
#                 stream = url.content
#                 data = load_yaml(stream, Loader=Loader)
#                 # Возвращает кортеж (object, created)
#                 shop_object, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
#                 for category in data['categories']:
#                     category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
#                     category_object.shops.add(shop_object.id)
#                     category_object.save()
#                 ProductInfo.objects.filter(shop_id=shop_object.id).delete()
#                 for item in data['goods']:
#                     product_object, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
#                     product_info = ProductInfo.objects.create(product_id=product_object.id,
#                                             external_id=item['id'],
#                                             model=item['model'],
#                                             price=item['price'],
#                                             price_rrc=item['price_rrc'],
#                                             quantity=item['quantity'],
#                                             shop_id=shop_object.id)
#                     for name, value in item['parameters'].items():
#                         parameter_object, _ = Parameter.objects.get_or_create(name=name)
#                         ProductParameter.objects.create(product_info_id=product_info.id,
#                                                         parameter_id=parameter_object.id,
#                                                         value=value)
#                 return Response({'Status': True})
#                 #return Response(data={'Status': True})
#         #return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
#         raise APIException(detail={'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            #return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
            raise NotAuthenticated(detail={'Status': False, 'Error': 'Log in required'})
        if request.user.type != 'shop':
            #return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)
            raise PermissionDenied(detail={'Status': False, 'Error': 'Только для магазинов'})
        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                data = load_yaml(stream, Loader=Loader)
                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info = ProductInfo.objects.create(product_id=product.id,
                                                              external_id=item['id'],
                                                              model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
