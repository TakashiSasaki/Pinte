OAUTH_PARAM_FILE = "../google-oauth-native-application.json"
SCOPE = ["email", "profile"]

import json
import urllib.request
import urllib.parse
import http.client
import webbrowser
from logging import getLogger
import time


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
        self.logger.debug("getUserCode")
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
        self.logger.debug("verifyUserCode")
        self.logger.debug("user_code = " + self.user_code)
        self.logger.debug("verification_url = %s" % self.verification_url)
        self.logger.debug("invoking web browser")
        webbrowser.open(self.verification_url, autoraise=True)
        self.logger.debug("opened web browser")

    def getAccessToken(self):
        while True:
            self.logger.debug("sleeping %s sec" % self.interval)
            time.sleep(self.interval)
            try:
                self.getAccessTokenOnce()
            except urllib.error.HTTPError as e:
                self.logger.debug(e)
                continue

    def getAccessTokenOnce(self):
        self.logger.debug("getAccessTokenOnce")
        data = {}
        data["client_id"] = self.client_id
        data["client_secret"] = self.client_secret
        data["code"] = self.device_code
        data["grant_type"] = "http://oauth.net/grant_type/device/1.0"
        self.logger.debug(data)
        response = urllib.request.urlopen("https://www.googleapis.com/oauth2/v3/token",
                                          bytes(urllib.parse.urlencode(data), "UTF-8"))
        assert isinstance(response, http.client.HTTPResponse)
        j = json.loads(response.readall().decode("UTF-8"))
        self.logger.debug("getAccessToken: %s" % str(j))
        self.access_token = j["access_token"]
        self.expires_in = j["expires_in"]
        self.refresh_token = j["refresh_token"]
        self.token_type = j["token_type"]

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
    device_flow.getAccessToken()
