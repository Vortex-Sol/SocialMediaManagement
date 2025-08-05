from django.shortcuts import render
from  .api_platforms.twitter_api import post_tweet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def post_page(request):
    return render(request, 'dashboard/index.html')

@csrf_exempt
def publish_to_twitter(request):
    print("Received request to publish_to_twitter")
    if request.method == 'POST':
        try:
            text = request.POST.get('description')
            image = request.FILES.get('image')

            image_path = None
            if image:
                image_path = f"/tmp/{image.name}"
                with open(image_path, 'wb+') as f:
                    for chunk in image.chunks():
                        f.write(chunk)

            success, tweet_id, tweet_url = post_tweet(text, image_path)

            if success:
                return JsonResponse({'status': 'success', 'tweet_url': tweet_url})
            else:
                return JsonResponse({'status': 'fail', 'error': 'Tweet failed'}, status=500)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'invalid'}, status=400)