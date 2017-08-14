#!C:\Users\sh\Anaconda3\python
from copy import deepcopy as dict_copy
import hashlib
import os
from datetime import datetime
import urllib
import requests
from furl import furl
import json
from selenium import webdriver
from configparser import ConfigParser
proj_dir = "C:\\Users\\sh\\Documents\\devbox\\github\\auto_invest"
conf_file = os.path.join(proj_dir, 'configuration.ini')


class SlackMessenger:
    config = ConfigParser()
    config.read(conf_file)
    _bot_user = config['BOT_USER']
    _oauth_authorize = config['OAUTH_AUTHORIZE']
    _oauth_access = config['OAUTH_ACCESS']
    _file_upload_url = config['FILE_UPLOAD_URL']
    _webhook = config['WEBHOOK']
    _client_id = config['CLIENT_ID']
    _client_secret = config['CLIENT_SECRET']
    _slack_domain = config['SLACK_DOMAIN']
    _slack_id = config['SLACK_ID']
    _slack_pw = config['SLACK_PW']
    _access_token = None
    _data = {
        "attachments": [
            {
                "channel": "@duke",
                "username": "AI",
                "icon_emoji": ":chart:",
                "color": "#764FA5"
            }
        ]
    }
    _headers = {'Content-type': 'application/json'}

    @classmethod
    def get_req(cls, uri, d, url_only=False):
        params = urllib.parse.urlencode(d)
        code_request_url = "%s?%s" % (uri, params)
        if url_only:
            return code_request_url
        else:
            opener = urllib.request.build_opener()
            request = urllib.request.Request(code_request_url)
            response = opener.open(request)
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read()
                data = json.loads(response_body)
            else:
                print("Error Code:" + rescode)
                data = None
            return data


    @classmethod
    def post_req(cls, uri, d):
        pass

    @classmethod
    def get_selenium_browser(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        return browser

    @classmethod
    def retrieve_access_token(cls, curr_invalid=False):
        if cls._access_token is None or curr_invalid:
            cls.get_access_token()
        return cls._access_token


    @classmethod
    def get_access_token(cls):
        authorize_params = {
            'client_id': cls._client_id,
            'scope': 'files:write:user',
            'team': cls._slack_domain
        }
        authorize_params.update({'state': hashlib.sha224(datetime.now().strftime("%b%d%Y%H:%M:%S").encode('utf-8')).hexdigest()})
        code_request_url = cls.get_req(cls._oauth_authorize, authorize_params, url_only=True)
        browser = cls.get_selenium_browser()
        browser.get(code_request_url)

        def fill_elems(b, d):
            for k, v in d.items():
                domain_name = b.find_element_by_id(k)
                domain_name.send_keys(v)

        def submit_login(b):
            login_attempt = b.find_element_by_xpath("//*[@type='submit']")
            login_attempt.submit()

        """phase one"""
        fill_elems(browser, {"domain": cls._slack_domain})
        submit_login(browser)
        """phase two"""
        fill_elems(browser, {"email": cls._slack_id
                             , "password": cls._slack_pw}
                   )
        submit_login(browser)
        """phase three"""
        submit_login(browser)

        """parse return code"""
        f = furl(browser.current_url)
        if f.args['state'] == authorize_params['state']:
            try:
                authorization_code = f.args['code']
            except KeyError as e:
                print('Response does not include code')
                return -1

        browser.quit()
        oauth_access_dict = {
            'client_id': cls._client_id,
            'client_secret': cls._client_secret,
            'code': authorization_code
        }
        res = cls.get_req(cls._oauth_access, oauth_access_dict)
        cls._access_token = res['access_token']
        return cls._access_token

    @classmethod
    def send_text(cls, text):
        payload = dict_copy(cls._data)
        payload['attachments'].update({'text': text})
        r = requests.post(cls._webhook, json=payload, headers=cls._headers)
        return r.status_code

    @classmethod
    def send_file(cls, title, channel, file):
        token = cls.retrieve_access_token()
        print(token)
        my_file = {'file': ('chart', open(file, 'rb'), 'image/jpg')}
        fields = {
            'token': token,
            'channels': ['#%s' % channel],
            'title': title,
        }
        headers = {'Content-type': "application/x-www-form-urlencoded"}
        r = requests.post(cls._file_upload_url, params=fields, files=my_file)
        print(r.text)
        return r.status_code

if __name__ == '__main__':
    text = 'testing slack messenger'
    image_url = "C:\\Users\\sh\\Pictures\\wallpapers\\ludwig-wittgenstein.jpg"
    title = 'ludwig-wittgenstein'
    print(SlackMessenger.send_file(title, image_url))
