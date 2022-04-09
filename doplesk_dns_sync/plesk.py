import subprocess
import re

class PleskManager:

  def __init__(self):
    self.__plesk = ["plesk", "bin"]
    pass

  def __exec(self, command):
    """
      Safely execute a OS command
      @params
        command = Required : list of arguments for command
    """
    result = subprocess.run(self.__plesk + command, stdout=subprocess.PIPE)
    return result.stdout.decode()

  def __parse_record(self, record):
    """
      Parses a DNS record
      @params
        record = Required : String of one line of DNS record
    """
    if "SUCCESS:" in record:
      return None
    record = re.sub("\s\s+", " ", record)
    spaced = record.split(" ")
    type = spaced[1]
    response = {
      "name": spaced[0],
      "type": type
    }
    if type in ["A", "AAAA", "CNAME", "NS"]:
      response['text'] = spaced[2]
    elif type == "MX":
      response['priority'] = spaced[2]
      response['text'] = spaced[3]
    elif type == "TXT":
      response['text'] = ' '.join(spaced[2:])
    elif type == "SRV":
      response['priority'] = spaced[2]
      response['port'] = spaced[4]
      response['text'] = spaced[5]
    return response

  def get_domains(self):
    """
      Fetches list of domains in Plesk
    """
    domains = self.__exec(['domain', '--list'])
    return list(filter(None, domains.split("\n")))

  def get_dns_records(self, domain): 
    """
      Gets all the dns records for a domain
      @params
        domain = Required : domain to get records for
    """
    response = self.__exec(['dns', '--info', domain])
    records = [line for line in response.split('\n') if line.strip() != '']
    dns = []
    for record in records:
      dns.append(self.__parse_record(record))
    return list(filter(None, dns))
    
    
      