from django.shortcuts import render
from myapp.models import Pet # xài lại model của myapp
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Tạo REST_API 

# Xài API 

# Thứ nhất phải là URL

# Tiếp theo là method: POST, GET, UPDATE, DELETE, PATCH, OPTIONS
# Ý nghĩa của các method: từ client gửi lên Server
# POST: Dùng trong trường hợp tạo mới 1 object
# GET: Dùng để đọc hết hoặc chi tiết của object
# PUT: Dùng để chỉnh sửa 1 object (cung cấp hết toàn bộ thuộc tính của đối tượng)
# DELETE: Dùng để xoá 1 object
# PATCH: Dùng để chỉnh sửa 1 object (Muốn chỉnh sửa gì đó thì bỏ vào)
# OPTION: Dùng để kiểm tra 1 URL, nó hỗ trợ mình những method nào.

# Status Code:
# Informational responses (100–199)

# Successful responses (200–299)
# 200 OK, 201 Create, 204 No content
# 200 OK là thành công
# 201 Create thì nó dành cho HTTP POST method
# 204 No content: chỉnh sửa

# Redirection messages (300–399)

# Client error responses (400–499)
# 400 Bad request: Data gửi lên lỗi
# 401 Unautherized: Chưa đăng nhập
# 403 Forbbiden: Không có quyền vào 1 resource nào đó
# 404 Not Found: object không tìm thấy
# 405 Method not allow: HTTP method với URL không được cho phép
# 408 Request time out: Server phản hồi chậm
# 409 Confict: Thông tin tạo mới sẽ xung đột với cái có sẵn

# Server error responses (500–599)
# 500 Internal Server:
# 502 Bad gate way (ĐKMH)
# 503 Service unavailable

# READ
# URL/API/PETS
# HTTP method: GET
# HTTP response code: 200 OK
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_list_pets(request):
    pets = Pet.objects.all()
    results = []
    for pet in pets:
        results.append({
            'id': pet.id,
            'name': pet.name,
            'age': pet.age,
            'type': pet.type,
            'length': pet.length,
            'color': pet.color,
            'weight': pet.weight,
            'vacinated': pet.vacinated,
            'dewormed': pet.dewormed,
            'sterilized': pet.sterilized,
        })
    return Response(data=results, status=200)

# READ
# URL/API/PETS
# HTTP method: GET
# HTTP response code: 
# 200 OK
# 404 Not found
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_detail_pets(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
        data =  {
                'id': pet.id,
                'name': pet.name,
                'age': pet.age,
                'type': pet.type,
                'length': pet.length,
                'color': pet.color,
                'weight': pet.weight,
                'vacinated': pet.vacinated,
                'dewormed': pet.dewormed,
                'sterilized': pet.sterilized,
            }
        return Response(data=data, status=200)
    except Pet.DoesNotExist:
        return Response(data={'error': f'Pet with {pet_id} not found'}, status=404)

# CREATE
# URL/API/PETS
# HTTP method: GET
# HTTP response code: 
# 201 OK
# 409 Confict
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_add_pet(request):
    try:
        pet_id = request.data['id']
        Pet.objects.get(id=pet_id)
        return Response(data={'error': f'Pet with {pet_id} already exist.'}, status=409)

    except Pet.DoesNotExist:
        pass
    Pet.objects.create(
                id = request.data['id'],
                name = request.data['name'],
                age = request.data['age'],
                type = request.data['type'],
                length = request.data['length'],
                color = request.data['color'],
                weight = request.data['weight'],
                vacinated = request.data['vacinated'],
                dewormed = request.data['dewormed'],
                sterilized = request.data['sterilized'],
    )

    return Response(status=201)

# UPDATE
# URL/API/PET/update/<pet_id>
# HTTP method: PUT
# HTTP response code: 
# 204 No content
# 404 Not found
# 400 Bad request
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def api_update_pet(request, pet_id):
    try:

        if set(request.data.keys()) != set(['id', 'name', 'age', 'type', 'length', 'color', 'weight', 'vacinated', 'dewormed', 'sterilized']):
            return Response(data={'error': 'Your data request is invalid'}, status=400)
        pet = Pet.objects.get(id=pet_id)
        pet.name = request.data['name']
        pet.age = request.data['age']
        pet.type = request.data['type']
        pet.length = request.data['length']
        pet.color = request.data['color']
        pet.weight = request.data['weight']
        pet.vacinated = request.data['vacinated']
        pet.dewormed = request.data['dewormed']
        pet.sterilized = request.data['sterilized']
        pet.save()
        return Response(status=204)
    except Pet.DoesNotExist:
        return Response(data={'error': f'Pet with {pet_id} not found'}, status=404)


# DELETE
# URL/API/PET/delete/<pet_id>
# HTTP method: DELETE
# HTTP response code: 
# 204 No content
# 404 Not found
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def api_delete_pet(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
        pet.delete()
        return Response(status=204)
    except Pet.DoesNotExist:
        return Response(data={'error': f'Pet with {pet_id} not found'}, status=404)

