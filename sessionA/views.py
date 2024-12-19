from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import Signup, ApiData
from .serializers import SignupSerializer, ApiDataSerializer
import requests

URL_LINK = "https://api.mfapi.in/mf/"

# Signup View
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(Password=make_password(serializer.validated_data['Password']))
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    def post(self, request):
        Name = request.data.get('Name')
        Password = request.data.get('Password')
        user = Signup.objects.filter(Name=Name).first()
        if user and check_password(Password, user.Password):
            request.session['Name'] = Name
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Home View
class HomeView(APIView):
    def get(self, request):
        if "Name" not in request.session:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        Name = request.session['Name']
        data = ApiData.objects.filter(Name=Name)
        serializer = ApiDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Add Data View
class AddView(APIView):
    def post(self, request):
        data = request.data
        Name = data.get('Name')
        fund_code = data.get('fund_code')
        Units_held = data.get('Units_held')
        Invested_Amount = data.get('Invested_Amount')

        # Fetch NAV details
        response = requests.get(URL_LINK + str(fund_code)).json()
        fund_name = response["meta"]["fund_house"]
        nav = float(response["data"][0]["nav"])
        current_value = nav * float(Units_held)
        Growth = current_value - float(Invested_Amount)

        new_data = {
            "Name": Name,
            "Invested_Amount": Invested_Amount,
            "fund_code": fund_code,
            "Units_held": Units_held,
            "fund_name": fund_name,
            "nav": nav,
            "current_value": current_value,
            "Growth": Growth,
        }
        serializer = ApiDataSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Edit Data View
class EditView(APIView):
    def post(self, request, id):
        instance = ApiData.objects.get(id=id)
        data = request.data

        # Fetch NAV details
        fund_code = data.get('fund_code', instance.fund_code)
        response = requests.get(URL_LINK + str(fund_code)).json()
        fund_name = response["meta"]["fund_house"]
        nav = float(response["data"][0]["nav"])
        current_value = nav * float(data.get('Units_held', instance.Units_held))
        Growth = current_value - float(data.get('Invested_Amount', instance.Invested_Amount))

        updated_data = {
            "Name": data.get('Name', instance.Name),
            "Invested_Amount": data.get('Invested_Amount', instance.Invested_Amount),
            "fund_code": fund_code,
            "Units_held": data.get('Units_held', instance.Units_held),
            "fund_name": fund_name,
            "nav": nav,
            "current_value": current_value,
            "Growth": Growth,
        }

        serializer = ApiDataSerializer(instance, data=updated_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Data View
class DeleteView(APIView):
    def post(self, request, id):
        instance = ApiData.objects.get(id=id)
        instance.delete()
        return Response({"message": "Data deleted successfully"}, status=status.HTTP_200_OK)

# Logout View
class LogoutView(APIView):
    def get(self, request):
        request.session.flush()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
