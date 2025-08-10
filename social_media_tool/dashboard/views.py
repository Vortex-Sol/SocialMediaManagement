import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# platform functions
from .api_platforms.twitter_api import post_tweet
from .api_platforms.pinterest_api import post_pin
from .api_platforms.facebook_api import post_facebook
from .api_platforms.instagram_api import post_insta
from .api_platforms.linkedin_api import post_linkedin


def post_page(request):
    return render(request, 'dashboard/index.html')


@csrf_exempt
def publish_to_twitter(request):
    """Legacy single-platform endpoint (kept so you don’t break anything while migrating)."""
    print("Received request to publish_to_twitter")
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid'}, status=400)
    try:
        text = request.POST.get('description')
        image = request.FILES.get('image')

        image_path = _save_temp_file(image) if image else None
        success, tweet_id, tweet_url = post_tweet(text, image_path)

        if success:
            return JsonResponse({'status': 'success', 'tweet_url': tweet_url})
        else:
            return JsonResponse({'status': 'fail', 'error': 'Tweet failed'}, status=500)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def publish_to_platforms(request):
    """
    New multi-platform endpoint.
    Expects:
      - description (str)
      - image (File, optional)
      - platforms (JSON array of strings): ["twitter","instagram","facebook","linkedin","pinterest"]
    Returns per-platform results.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid'}, status=400)

    try:
        text = (request.POST.get('description') or '').strip()
        if not text:
            return JsonResponse({'status': 'error', 'message': 'Description is required.'}, status=400)

        # Parse platforms
        platforms_raw = request.POST.get('platforms', '[]')
        try:
            platforms = json.loads(platforms_raw)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid platforms payload.'}, status=400)

        if not isinstance(platforms, list) or not platforms:
            return JsonResponse({'status': 'error', 'message': 'Select at least one platform.'}, status=400)

        image = request.FILES.get('image')
        image_path = _save_temp_file(image) if image else None

        # platforms that *require* an image
        requires_image = {'instagram', 'pinterest'}

        results = {}
        for platform in platforms:
            platform = (platform or '').lower().strip()
            if platform not in {'twitter', 'facebook', 'instagram', 'linkedin', 'pinterest'}:
                results[platform or ''] = {
                    'status': 'error',
                    'error': 'Unknown platform'
                }
                continue

            if platform in requires_image and not image_path:
                results[platform] = {
                    'status': 'skipped',
                    'reason': 'This platform requires an image.'
                }
                continue

            try:
                res = _dispatch_post(platform, text, image_path)
                results[platform] = res
            except NotImplementedError:
                results[platform] = {
                    'status': 'skipped',
                    'reason': 'Not implemented yet.'
                }
            except Exception as e:
                results[platform] = {
                    'status': 'error',
                    'error': str(e)
                }

        # Cleanup temp file
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass

        return JsonResponse({'status': 'ok', 'results': results})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def _save_temp_file(django_file):
    """Save uploaded file to /tmp and return its path."""
    if not django_file:
        return None
    path = f"/tmp/{django_file.name}"
    with open(path, 'wb+') as f:
        for chunk in django_file.chunks():
            f.write(chunk)
    return path


def _dispatch_post(platform, text, image_path):
    """
    Call the right function and normalize its return into:
      { status: 'success'|'error', id?: str, url?: str, message?: str, error?: str }
    """
    if platform == 'twitter':
        success, post_id, url = post_tweet(text, image_path)
        if success:
            return {'status': 'success', 'id': post_id, 'url': url}
        return {'status': 'error', 'error': 'Failed to post tweet.'}

    if platform == 'pinterest':
        success, post_id, url = post_pin(text, image_path)
        if success:
            return {'status': 'success', 'id': post_id, 'url': url}
        return {'status': 'error', 'error': 'Failed to create pin.'}

    if platform == 'facebook':
        # not implemented yet in your code
        result = post_facebook(text, image_path)
        if result is NotImplemented:
            raise NotImplementedError
        return _normalize_generic_result(result)

    if platform == 'instagram':
        result = post_insta(text, image_path)
        if result is NotImplemented:
            raise NotImplementedError
        return _normalize_generic_result(result)

    if platform == 'linkedin':
        result = post_linkedin(text, image_path)
        return _normalize_generic_result(result)

    raise ValueError('Unknown platform')


def _normalize_generic_result(result):
    """
    Helper for future FB/IG/LinkedIn implementations.
    Accepts any of:
      - (success: bool, id, url) tuple
      - dict with keys: success, id, url, message, error
    Returns our normalized dict.
    """
    if isinstance(result, tuple) and len(result) >= 1:
        success = bool(result[0])
        post_id = result[1] if len(result) > 1 else None
        url = result[2] if len(result) > 2 else None
        return {'status': 'success', 'id': post_id, 'url': url} if success else {'status': 'error', 'error': 'Posting failed.'}

    if isinstance(result, dict):
        if result.get('success'):
            return {'status': 'success', 'id': result.get('id'), 'url': result.get('url'), 'message': result.get('message')}
        return {'status': 'error', 'error': result.get('error') or 'Posting failed.'}

    # fallback
    return {'status': 'error', 'error': 'Unexpected return format from platform function.'}
