from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def analyze(request):
    timestamps = request.data.get('timestamps', [])
    if len(timestamps) < 2:
        return Response({'riskScore': 0.0})
    intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    variance = sum(abs(i - 200) for i in intervals) / len(intervals)
    risk = min(1.0, variance / 500)
    return Response({'riskScore': risk})
