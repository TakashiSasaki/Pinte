OAUTH_PARAM_FILE = "../google-oauth-native-application.json"
SCOPE = ["email", "profile"]

import json
import urllib.request
import urllib.parse
import http.client


class DeviceFlow(object):
    def __init__(self, oauth_params):
        if isinstance(oauth_params, str):
            f = open(oauth_params)
            self.oauthParams = json.load(f)
        elif isinstance(oauth_params, dict):
            self.oauthParams = oauth_params
        if "installed" not in self.oauthParams:
            raise RuntimeError("no 'installed' key in given dict")

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
    device_flow = DeviceFlow(OAUTH_PARAM_FILE)
    device_flow.getUserCode(SCOPE)