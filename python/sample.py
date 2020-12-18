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
 
    def get_system_info(self): 
        data = {"jsonrpc": "2.0", "method": "get_system_info",
                "params": {

                          },
                "filter": self.genericfilter
                }
        logging.info(u'get_system_info method call')
        return self.send_request(data)
 
    def get_status(self): 
        data = {"jsonrpc": "2.0", "method": "get_status",
                "params": {

                          },
                "filter": self.genericfilter
                }
        logging.info(u'get_status method call')
        return self.send_request(data)
 
    def set_status(self, status, mood): 
        data = {"jsonrpc": "2.0", "method": "set_status",
                "params": {
                     'status': status,
                     'mood': mood
                          },
                "filter": self.genericfilter
                }
        logging.info(u'set_status method call')
        return self.send_request(data)
 
    def make_payment(self, from_wallet, to_wallet, amount, comment): 
        data = {"jsonrpc": "2.0", "method": "make_payment",
                "params": {
                     'from_wallet': from_wallet,
                     'to_wallet': to_wallet,
                     'amount': amount,
                     'comment': comment
                          },
                "filter": self.genericfilter
                }
        logging.info(u'make_payment method call')
        return self.send_request(data)
