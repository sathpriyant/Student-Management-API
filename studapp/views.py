from django.shortcuts import render
from rest_framework.response import Response
from studapp.models import StudentDb
from studapp.serializer import StudentSerializer,RegistationSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,AllowAny


# Create your views here.




class StudentCreateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = StudentDb.objects.all()
        serializer_instance = StudentSerializer(students, many=True)
        return Response(serializer_instance.data)

    def post(self, request):
        serializer_instance = StudentSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "message": "Student added successfully",
                "student": serializer_instance.data
            })
        else:
            return Response(serializer_instance.errors)


class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return StudentDb.objects.get(id=pk)
        except StudentDb.DoesNotExist:
            return None

    def get(self, request, pk):
        student = self.get_object(pk)

        serializer_instance = StudentSerializer(student)
        return Response(serializer_instance.data)

    def put(self, request, pk):
        student = self.get_object(pk)

        serializer_instance = StudentSerializer(student, data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)

        return Response(serializer_instance.errors)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response({"message": "Student deleted successfully"})

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer_instance = RegistationSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message": "Registered"})
        else:
            return Response(data=serializer_instance.errors)

        