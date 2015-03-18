import json
import urllib.request
import urllib.error
import urllib.response
import urllib.parse
import http.client


class WebApplicationFlow(object):
    def __init__(self, oauth_params):
        assert isinstance(oauth_params, dict)
        if "web" not in oauth_params: raise RuntimeError("no 'web' key in given dict")
        self.oauthParams = oauth_params

    def getAuthUrl(self, scope_list, state):
        assert isinstance(scope_list, list)
        assert isinstance(state, str)
        self.authUrl = self.oauthParams["web"]["auth_uri"]
        self.authUrl += "?response_type=code"
        self.authUrl += "&client_id=" + self.oauthParams["web"]["client_id"]
        self.authUrl += "&redirect_uri=" + self.oauthParams["web"]["redirect_uris"][0]
        self.authUrl += "&scope=" + "%20".join(scope_list)
        self.authUrl += "&state=" + state
        self.authUrl += "&access_type=offline"
        self.authUrl += "&include_granted_scopes=true"


class InstalledApplicationFlow(object):
    def __init__(self, oauth_params):
        assert isinstance(oauth_params, dict)
        if "installed" not in oauth_params: raise RuntimeError("no 'installed' key in given dict")
        self.oauthParams = oauth_params


class DeviceFlow(object):
    def __init__(self, oauth_params):
        assert isinstance(oauth_params, dict)
        if "installed" not in oauth_params: raise RuntimeError("no 'installed' key in given dict")
        self.oauthParams = oauth_params

    def getUserCode(self, scope):
        assert isinstance(scope, list)
        data = {}
        data["client_id"] = self.oauthParams["installed"]["client_id"]
        data["scope"] = " ".join(scope)
        response = urllib.request.urlopen("https://accounts.google.com/o/oauth2/device/code",
                                          bytes(urllib.parse.urlencode(data), "UTF-8"))
        assert isinstance(response, http.client.HTTPResponse)
        j = json.loads(response.readall().decode("UTF-8"))
        self.interval = j["interval"]
        self.verification_url = j["verification_url"]
        self.device_code = j["device_code"]
        self.user_code = j["user_code"]
        self.expires_in = j["expires_in"]


if __name__ == "__main__":
    print("GoogleOauth.py")
    native_oauth_params_file = open("google-oauth-native-application.json")
    native_oauth_params = json.load(native_oauth_params_file)
    for x in native_oauth_params["installed"]:
        print(x, native_oauth_params["installed"][x])

    device_flow = DeviceFlow(native_oauth_params)
    device_flow.getUserCode(["email", "profile"])
    print(device_flow.user_code)

    web_oauth_params_file = open("google-oauth-web-application.json")
    web_oauth_params_params = json.load(web_oauth_params_file)["web"]
    for x in web_oauth_params_params:
        print(x, web_oauth_params_params[x])
