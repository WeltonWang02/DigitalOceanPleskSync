import plesk
import digitalocean
import os
from dotenv import load_dotenv

load_dotenv()

pm = plesk.PleskManager()
do = digitalocean.DigitalOceanManager(os.getenv("DO_API_KEY"), os.getenv("DO_TTL"))

def full_sync():
  """
    Sync DNS records for all domains
  """
  domains = pm.get_domains()
  for domain in domains:
    
    try:
      do.delete_domain(domain)
      do.add_domain(domain)
    except (digitalocean.HTTPResponseException, digitalocean.HTTPRateLimitException) as e:
      print (f"Error thrown when adding domain: {domain}.\nError: {str(e)}")
      
    dns = pm.get_dns_records(domain)
    
    for record in dns:
      try:
        do.add_record(domain, **record)
      except (digitalocean.HTTPResponseException, digitalocean.HTTPRateLimitException) as e:
        print (f"Error thrown when adding record for {domain}.\nError: {str(e)}\nRecord: {record}")

  print("Finished")

def single_sync(domain):
  """
    Sync DNS records for one domain
    @params
      domain = Required : domain to sync records for
  """
  try:
    do.delete_domain(domain)
    do.add_domain(domain)
  except (digitalocean.HTTPResponseException, digitalocean.HTTPRateLimitException) as e:
    print (f"Error thrown when adding domain: {domain}.\nError: {str(e)}")
      
  dns = pm.get_dns_records(domain)
  
  for record in dns:
    try:
      do.add_record(domain, **record)
    except (digitalocean.HTTPResponseException, digitalocean.HTTPRateLimitException) as e:
      print (f"Error thrown when adding record for {domain}.\nError: {str(e)}\nRecord: {record}")

  print("Finished")
