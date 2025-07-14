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

            if not timestamps or len(timestamps) < 2:
                return JsonResponse({'error': 'Not enough data'}, status=400)

            intervals = np.diff(timestamps)
            risk_score = float(np.std(intervals) / (np.mean(intervals) + 1e-6))
            risk_score = min(max(risk_score, 0.0), 1.0)

            return JsonResponse({'riskScore': round(risk_score, 2)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({"message": "Analyze endpoint is live. Use POST with timestamps."})
