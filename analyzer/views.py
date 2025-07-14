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
                return JsonResponse({'riskScore': 0.1})  # Very low risk due to insufficient data

            # Calculate typing intervals
            gaps = np.diff(timestamps)
            
            # Clip out extremely small or long gaps (e.g., noise, pauses)
            gaps = np.clip(gaps, 50, 2000)  # ms

            mean_gap = np.mean(gaps)
            std_gap = np.std(gaps)

            # Normalize the std deviation and offset to ignore minor fluctuations
            normalized_std = std_gap / (mean_gap + 1e-6)

            # Risk score logic: tolerate normal human variation
            adjusted_score = max(0.0, (normalized_std - 0.1) * 2)
            risk_score = round(min(adjusted_score, 1.0), 2)

            return JsonResponse({'riskScore': risk_score})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
