import json

def getAuthUrl(oauth_params, scope_list, state):
    assert isinstance(oauth_params, dict)
    assert isinstance(scope_list, list)
    assert isinstance(state, str)
    if "installed" not in oauth_params: raise RuntimeError("no 'installed' key in give dict")
    s = oauth_params["installed"]["auth_uri"]
    s += "?response_type=code"
    s += "&client_id=" + oauth_params["installed"]["client_id"]
    s += "&redirect_uri=" + oauth_params["installed"]["redirect_uris"][0]
    s += "&scope=" + "%20".join(scope_list)
    s += "&state=" + state
    s += "&access_type=offline"
    s += "&include_granted_scopes=true"
    return s

if __name__ == "__main__":
    print("GoogleOauth.py")
    native_oauth_params_file = open("google-oauth-native-application.json")
    native_oauth_params = json.load(native_oauth_params_file)
    for x in native_oauth_params["installed"]:
        print(x, native_oauth_params["installed"][x])

    print(getAuthUrl(native_oauth_params, ["email", "profile"], "abcde_state_abcde"))

    web_oauth_params_file = open("google-oauth-web-application.json")
    web_oauth_params_params = json.load(web_oauth_params_file)["web"]
    for x in web_oauth_params_params:
        print(x, web_oauth_params_params[x])
