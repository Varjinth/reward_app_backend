from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed



class RegisterView(APIView):
    def post(self, request):
        data=request.data
        data["username"] = data["email"]
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        print(request.data)


        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)

            response = Response({
                "message": "Login successful",
                "role": user.role,
            })
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite="None"
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="None"
            )
            response.set_cookie(
                key="role",
                value=user.role,
                httponly=True,
                secure=True,
                samesite="None"
            )
            return response

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logout successful"})
        response.delete_cookie("access_token", samesite="None")
        response.delete_cookie("refresh_token", samesite="None")
        response.delete_cookie("role", samesite="None")
        return response


def check_authentication(request):
    auth = JWTAuthentication()
    raw_token = request.COOKIES.get("access_token")

    if not raw_token:
        return JsonResponse({"authenticated": False, "error": "No token provided"}, status=401)

    try:
        validated_token = auth.get_validated_token(raw_token)
        user = auth.get_user(validated_token)
        return JsonResponse({"authenticated": True, "role": user.role})
    except AuthenticationFailed:
        return JsonResponse({"authenticated": False, "error": "Invalid token"}, status=401)


class AppListCreateAPIView(APIView):
    """
    Handles listing all apps, creating a new app and deleting an app.
    Only authenticated users can access.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = App.objects.all()
        serializer = AppSerializer(apps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        app = App.objects.get(id=pk)
        app.delete()
        return Response({"message": "App deleted successfully"}, status=status.HTTP_200_OK)


class UserTaskCreateAPIView(APIView):
    """
    Handles creating a new user completed task.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        app_id = request.data.get("app_id")

        if not app_id:
            return Response({"error": "app_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            app = App.objects.get(id=app_id)  # Ensure app exists
        except App.DoesNotExist:
            return Response({"error": "Invalid app_id."}, status=status.HTTP_400_BAD_REQUEST)

        existing_task = UserTask.objects.filter(user=request.user, app=app).first()
        if existing_task:
            return Response({"error": "You have already completed this task."}, status=status.HTTP_400_BAD_REQUEST)



        serializer = UserTaskSerializer(data=request.data)
        print("i am printed")
        if serializer.is_valid():
            serializer.save(user=request.user, app=app, completed=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompletedTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch completed tasks for the logged-in user."""
        completed_tasks = UserTask.objects.filter(user=request.user, completed=True)
        serializer = UserTaskSerializer(completed_tasks, many=True, context={"request": request})
        return Response(serializer.data)

class PendingTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch pending tasks for the logged-in user by excluding completed ones."""
        completed_task_ids = UserTask.objects.filter(user=request.user, completed=True).values_list('app_id', flat=True)

        # Get all apps but exclude those in completed tasks
        pending_tasks = App.objects.exclude(id__in=completed_task_ids)
        serializer = AppSerializer(pending_tasks, many=True)

        return Response(serializer.data)

class UserDetailsView(APIView):
    """Fetch user details including username and total points earned.

    - If the user is an admin, return all users' details.
    - Otherwise, return only the requested user's details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'admin':
            users_data = []

            users = User.objects.all()
            for user in users:
                completed_tasks = UserTask.objects.filter(user=user, completed=True)
                total_points = sum(task.app.points for task in completed_tasks)

                users_data.append({
                    "username": user.first_name,
                    "points_earned": total_points
                })
                users_data.sort(key=lambda x: x["points_earned"], reverse=True)

            return Response(users_data)

        else:
            user = request.user
            completed_tasks = UserTask.objects.filter(user=user, completed=True)
            total_points = sum(task.app.points for task in completed_tasks)

            user_data = {
                "name": user.first_name,
                "points": total_points
            }

            return Response(user_data)