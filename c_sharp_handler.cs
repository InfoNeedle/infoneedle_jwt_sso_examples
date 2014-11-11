// Handler: <%@ WebHandler Language="C#" Class="InfoNeedle.JWTLogin" CodeBehind="InfoNeedle.JWTLogin.cs" %>
// Requires: JWT (https://nuget.org/packages/JWT)
// Tested with .NET 4.5

using System;
using System.Web;
using System.Collections.Generic;

namespace InfoNeedle
{
    public class JWTLogin : IHttpHandler
    {
        private const string SHARED_KEY = "{my infoneedle token}";
        private const string VENUE_ID = "{my infoneedle venue_id}";

        public void ProcessRequest(HttpContext context)
        {
            TimeSpan t = (DateTime.UtcNow - new DateTime(1970, 1, 1));
            int timestamp  = (int) t.TotalSeconds;

            var payload = new Dictionary<string, object>() {
                { "iat", timestamp },
                { "jti", System.Guid.NewGuid().ToString() }
                // { "first_name", currentUser.firstName },
                // { "email", currentUser.email }
            };

            string token = JWT.JsonWebToken.Encode(payload, SHARED_KEY, JWT.JwtHashAlgorithm.HS256);
            string redirectUrl = "https://www.infoneedle.com/access/" + VENUE_ID + "/jwt?jwt=" + token;

            string returnTo = context.Request.QueryString["return_to"];

            if(returnTo != null) {
              redirectUrl += "&return_to=" + HttpUtility.UrlEncode(returnTo);
            }

            context.Response.Redirect(redirectUrl);
        }

        public bool IsReusable
        {
            get
            {
                return true;
            }
        }
    }
}
