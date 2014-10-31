# This example relies on you having install PyJWT, `sudo easy_install PyJWT` - you can
# read more about this in the GitHub repository https://github.com/progrium/pyjwt

from django.http import HttpResponseRedirect

import time
import jwt
import uuid
import urllib

def index(request):

  payload = {
    "iat": int(time.time()),
    "jti": str(uuid.uuid1()),
    "name": request.user.get_full_name(),
    "email": request.user.email
  }

  venue_id  = "{my infoneedle venue_id}"
  shared_key = "{my infoneedle token}"
  jwt_string = jwt.encode(payload, shared_key)
  location = "https://www.infoneedle.com/access/" + venue_id + "/jwt?jwt=" + jwt_string
  return_to = request.GET.get('return_to')

  if return_to is not None:
    location += "&return_to=" + urllib.quote(return_to)

  return HttpResponseRedirect(location)
