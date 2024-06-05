from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from medical.models import Medicine
from medical_api.serializers import MedicineSerializer, UserSerializer

# Signup API view
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API view
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Create Medicine API view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medicine(request):
    serializer = MedicineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve Medicine API view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_medicine(request, pk):
    try:
        medicine = Medicine.objects.get(pk=pk, user=request.user)
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Medicine.DoesNotExist:
        return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)

# Update Medicine API view
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine(request, pk):
    try:
        medicine = Medicine.objects.get(pk=pk, user=request.user)
        serializer = MedicineSerializer(medicine, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Medicine.DoesNotExist:
        return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)

# Delete Medicine API view
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medicine(request, pk):
    try:
        medicine = Medicine.objects.get(pk=pk, user=request.user)
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Medicine.DoesNotExist:
        return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)