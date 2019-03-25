from __future__ import unicode_literals
import json
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from inventory.models import Users, Item, Variant, Audit
from inventory.serializers import ItemSerializer, UsersSerializer, VariantSerializer

class UsersView(APIView):
    def post(self, request):
        try:
            user_details = json.loads(request.body)
            user = Users(**user_details)
            user.save()
            return Response({'obj': user_details}, status=200)
        except Exception:
            response_dict = {
                'message': 'Internal server error',
                'status_code': 500
            }
            print('Internal server error [{}]'.format(traceback.format_exc()))
        return Response(response_dict, status=response_dict['status_code'])

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = Users.objects.get(id=user_id)
        return Response(user.get_dict(), status=200)

class InventoryView(APIView):
    def post(self, request):
        try:
            inventory = json.loads(request.body)
            serializer = ItemSerializer(data=inventory)

            if serializer.is_valid():
                serializer.save()
                response_dict = {'message': serializer.data, 'status_code': 200}
            else:
                response_dict = {'message': serializer.errors, 'status_code': 401}
        except:
            print(traceback.format_exc())
            response_dict = {'message': 'Internal server error', 'status_code': 500}
        return Response(response_dict, status=response_dict['status_code'])

    def get(self, request):
        try:
            product_code = request.GET.get('product_code')
            inventory = Item.objects.get(product_code=product_code)
            serializer = ItemSerializer(inventory)
            response_dict = {'item': serializer.get_json_data(), 'status_code': 200}
        except Item.DoesNotExist:
            response_dict = {
                'message': 'No item found for product_code {}'.format(product_code),
                'status_code': 404
            }
        except:
            print(traceback.format_exc())
            response_dict = {'message': 'Internal server error', 'status_code': 500}
        return Response(response_dict, status=response_dict['status_code'])

class VariantView(APIView):
    def post(self, request):
        try:
            variant = json.loads(request.body)
            serializer = VariantSerializer(data=variant)

            if serializer.is_valid():
                serializer.save()
                response_dict = {'message': serializer.data, 'status_code': 200}
            else:
                response_dict = {'message': serializer.errors, 'status_code': 401}
        except:
            print(traceback.format_exc())
            response_dict = {'message': 'Internal server error', 'status_code': 500}
        return Response(response_dict, status=response_dict['status_code'])
    
    def get(self, request):
        try:
            id = int(request.GET.get('id'))
            variant = Variant.objects.get(id=id)
            serializer = VariantSerializer(variant)
            response_dict = {'variant': serializer.data, 'status_code': 200}
        except:
            print(traceback.format_exc())
            response_dict = {'error': 'Internal server error', 'status_code': 500}
        return Response(response_dict, status=response_dict['status_code'])
    