import sys, argparse
import sync
import os 

def run():
  """
    Main function routine
  """
  args = sys.argv
  
  parser = argparse.ArgumentParser(prog='doplesk_dns_sync/main.py', description='Synchronized domain\'s DNS records in Plesk with DigitalOcean')
  parser.add_argument('command', type=str, help='full_sync or single_sync')
  parser.add_argument('-d', dest='domain', type=str, required=False, help='domain to synchronize if single_sync')
  
  args = parser.parse_args()

  if not os.getenv("DO_API_KEY") or not os.getenv("DO_TTL"):
    print("Please set the DO_API_KEY and DO_TTL environment variables in .env")
    return
    
  if args.command == "single_sync":
    if not args.domain:
      print("Please pass a domain as -d. See --help for more information")
      return
    domain = args.domain
    sync.single_sync(domain)
  elif args.command == "full_sync":
    sync.full_sync()
  else:
    print("Invalid command, choose full_sync or single_sync.")

if __name__ == "__main__":
  run()
