#!/usr/bin/env python

class Sample(object):

    def __init__(self, apiurl, token, delay=0.5):
        self.apiurl = apiurl
        self.token = token
        self.delay = delay
        self.extrainfo = ''
        self.generic_filter = {"sortBy": "", "offset": "", "limit": ""}

    def send_request(self, data):
        try:
            time.sleep(self.delay)
            self.extrainfo = ''
            headers = {}
            data["token"] = self.token
            
            req = requests.post(self.apiurl, json.dumps(data).encode("utf-8"), headers=headers)
            
            logging.debug(req.status_code)
            logging.debug(req.reason)
            if req.status_code != 200:
                logging.error(u'Request status error')
                return False, "Request status error, may be too Many Requests"
                
            j = json.loads(req.text)
            
            if "result" not in j:
                logging.debug(u'Wrong response data')
                return False, j["error"]
            else:
                self.extrainfo = j["resultExtraInfo"]
                return True, j["result"]
            
        except Exception as e:
            logging.error(u'This is an exception. Message:')
            logging.error(e)
            return False, ""

    def generic_filter_set(self, sortby, offset, limit):
        self.generic_filter = {"sortBy": sortby,
                               "offset": offset,
                               "limit": limit}

    def generic_filter_clear(self):
        self.generic_filter = {"sortBy": "", "offset": "", "limit": ""}

    def get_extra_info(self):
        return self.extrainfo
