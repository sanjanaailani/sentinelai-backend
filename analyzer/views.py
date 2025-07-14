from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np

@csrf_exempt
def analyze(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            timestamps = data.get('timestamps', [])

            if len(timestamps) < 2:
                return JsonResponse({'riskScore': 0.1})  # Very low

            gaps = np.diff(timestamps)
            risk = min(1.0, np.std(gaps) / 500)  # Normalize std dev

            return JsonResponse({'riskScore': round(float(risk), 2)})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
