from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView


from user_profile.models import UserProfile
from .serializer import ImageModelSerializer
from .models import ImageModel
# Create your views here.




class GetAllImagesForProfile(APIView):    
    def post(self, request):
        try:
            user_profile = UserProfile.objects.filter(id=request.data["profile"])
        except ObjectDoesNotExist:
            print("User Profile does not exist")
            return HttpResponse(status=400)
             
        try:
            images = ImageModel.objects.filter(profile=user_profile)
        except ObjectDoesNotExist:
            print("Profile does not have images")
            return HttpResponse(status=400)
        
        serializer = ImageModelSerializer(images)
        return JsonResponse(serializer.data, safe=False)
