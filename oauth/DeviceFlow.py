OAUTH_PARAM_FILE = "../google-oauth-native-application.json"
SCOPE = ["email", "profile"]

import json
import urllib.request
import urllib.parse
import http.client
import webbrowser
from logging import getLogger


class DeviceFlow(object):
    logger = getLogger("DeviceFlow")

    def __init__(self, oauth_params):
        if isinstance(oauth_params, str):
            f = open(oauth_params)
            self.oauthParams = json.load(f)
        elif isinstance(oauth_params, dict):
            self.oauthParams = oauth_params
        if "installed" not in self.oauthParams:
            raise RuntimeError("no 'installed' key in given dict")

        self.client_id = self.oauthParams["installed"]["client_id"]
        self.client_secret = self.oauthParams["installed"]["client_secret"]

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

    def verifyUserCode(self):
        self.logger.warning("user_code = " + self.user_code)
        self.logger.warning("verification_url = %s" % self.verification_url)
        webbrowser.open(self.verification_url, autoraise=True)

    def getAccessToken(self):
        data = {}
        data["client_id"] = self.client_id
        data["client_secret"] = self.client_secret
        data["code"] = self.device_code
        data["grant_type"] = "http://oauth.net/grant_type/device/1.0"
        response = urllib.request.urlopen("https://www.googleapis.com/oauth2/v3/token",
                                          bytes(urllib.parse.urlencode(data), "UTF-8"))
        assert isinstance(response, http.client.HTTPResponse)
        j = json.loads(response.readall().decode("UTF-8"))
        print(j)

    def getAccessTokenRepeatedly(self):
        pass

    def testLog(self):
        self.logger.debug("testLog debug")
        self.logger.info("testLog info")
        self.logger.warning("testLog warning")
        self.logger.error("testLog error")
        self.logger.critical("testLog critical")


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    device_flow = DeviceFlow(OAUTH_PARAM_FILE)
    device_flow.testLog()
    device_flow.getUserCode(SCOPE)
    device_flow.verifyUserCode()
