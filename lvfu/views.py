from datetime import date, timedelta

from django.http import HttpResponse


def fb_channel(request):
    response = HttpResponse('<script src="//connect.facebook.net/en_US/all.js"></script>',
                            mimetype='text/html')
    seconds = 31449600  # 364 days
    maxage = timedelta(seconds=seconds)
    expires = date.today() + maxage
    response['Pragma'] = 'public'
    response['Cache-Control'] = 'max-age=' + str(seconds)
    response['Expires'] = expires.strftime("%a, %d %b %Y 20:00:00 GMT")
    return response
