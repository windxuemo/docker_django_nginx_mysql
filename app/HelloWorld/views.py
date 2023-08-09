from django.http import JsonResponse


# Create your views here.
def get_data(request):
    data = {
        "message": "This is data from the API.",
        "value": 42
    }
    return JsonResponse(data)
