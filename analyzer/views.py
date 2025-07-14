
from django.http import JsonResponse
from rest_framework.decorators import api_view
import numpy as np

@api_view(["POST"])
def analyze(request):
    timestamps = request.data.get("timestamps", [])

    if len(timestamps) < 2:
        return JsonResponse({"riskScore": 0.0})

    # Convert to milliseconds, then calculate time differences
    time_diffs = np.diff(timestamps)
    avg_speed = np.mean(time_diffs)

    # Risk logic: faster typing → lower risk, erratic → higher risk
    std_dev = np.std(time_diffs)
    risk_score = min(1.0, std_dev / 200)  # Normalize to 0-1 range

    return JsonResponse({"riskScore": round(float(risk_score), 2)})
