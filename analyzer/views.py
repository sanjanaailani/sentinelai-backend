from django.http import JsonResponse

def analyze(request):
    return JsonResponse({"message": "Analyze endpoint is working"})
