# This example relies on you having installed PyJWT, `sudo easy_install PyJWT` - you can
# read more about this in the GitHub repository https://github.com/progrium/pyjwt

from flask import Flask, request, redirect
import time
import uuid
import jwt
import urllib

# insert token here
app.config['SHARED_KEY'] = ''
# insert venue id here
app.config['VENUE_ID'] = 'yoursite'

@app.route('/infoneedle-jwt')
def sso_redirector():

	payload = {
		"iat": int(time.time()),
		"jti": str(uuid.uuid1()),
		# populate these values from your data source
		"name": '',
		"email": ''
	}

	jwt_string = jwt.encode(payload, app.config['SHARED_KEY'])
	sso_url = "https://www.infoneedle.com/access/" + app.config ['VENUE_ID'] + "/jwt?jwt=" + jwt_string
        return_to = request.args.get('return_to')

        if return_to is not None:
            sso_url += "&return_to=" + urllib.quote(return_to)

	return redirect(sso_url)

if __name__ == "__main__":
	app.run()
