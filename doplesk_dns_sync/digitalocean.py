import requests
import time
import ratelimit

class HTTPResponseException(Exception):
    """Unexpected HTTP Response from API"""
    pass

class HTTPRateLimitException(Exception):
    """429 HTTP Response from API"""
    pass
  
class DigitalOceanManager:
  
  def __init__(self, token, ttl):
    """
      Initialize authentication data
    """
    self.__api = token
    self.__auth = {
      "Authorization": f"Bearer {token}"
    }
    self.__url = "https://api.digitalocean.com/v2/domains"
    self.__ttl = ttl

  @ratelimit.sleep_and_retry
  @ratelimit.limits(calls=250, period=60)
  def __api_call(self, path, method, data):  
    """
      Handle a rate-limited call to DO API
      @params
        path = Required : URL route to call
        method = Required : HTTP Method to use
        data = Required : dict of to-be JSON Encoded data
    """
    response = requests.request(
      method, 
      headers = self.__auth,
      url = self.__url + path,
      json = data
    )
    return response

  def __handle_http_response(self, response):
    """
      Handle HTTP Requests
      @params
        response = Required : requests response object
    """
    if response.status_code == 429:
      raise HTTPRateLimitException(f"429 Rate Limited")
    if response.status_code not in [201, 204]:
      raise HTTPResponseException(f"Invalid HTTP Response {response.status_code}: {response.json()['message']}")
    return response
  
  def add_domain(self, domain):
    """
      Adds a domain to DO
      @params
        domain = Required : domain to add
    """
    response = self.__api_call("/", "POST", {"name":domain})
    self.__handle_http_response(response)
    return True

  def delete_domain(self, domain):
    """
      Removes a domain from DO
      @params
        domain = Required : domain to remove
    """
    response = self.__api_call(f"/{domain}", "DELETE", {"name":domain})
    self.__handle_http_response(response)
    return True

  def __insert_dns_record(self, domain, data): 
    """
      Inserts a DNS record for a domain (helper)
      @params
        domain = Required : domain to insert record for
        data = Required : dictionary of DNS record
    """
    response = self.__api_call(f"/{domain}/records", "POST", data)
    self.__handle_http_response(response)
    return True

  def add_record(self, domain, type, name, text, **kwargs):
    """
      Adds a DNS record
      @params
        domain = Required : domain to add record for
        type = Required : record type [A, AAAA, CNAME, TXT, ...]
        name = Required : reecord name, either prefix before domain, or full name with trailing . (dot)
        text = Required : target of record (IP, Text, Hostname, ...)
        priority = Optional : record priority for MX/SRV
        port = Optional : port for SRV
        weight = Optional : weight for SRV
    """
    data = {
      "type": type,
      "name": name,
      "data": text,
      "priority": kwargs.get('priority', None),
      "port": kwargs.get('port', None ),
      "ttl": self.__ttl,
      "weight": kwargs.get('weight', None ),
      "flags": kwargs.get('flags', None ),
      "tag": kwargs.get('tag', None )
    }
    self.__insert_dns_record(domain, data)      
    
    
  

  
  
    
    
