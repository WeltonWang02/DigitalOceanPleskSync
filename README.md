
# Synchronize Plesk DNS Records with DigitalOcean

In light of #EXTPLESK-3432, the following will properly synchronize all DNS records with DigitalOcean, deleting any garbled records.

### Usage

To install required packages:

```pip3 install -r requirements.txt```

Create an ```.env``` file with the following:

```
DO_API_KEY=<DIGITALOCEAN_API_KEY>
DO_TTL=<DNS_TTL_IN_SECONDS>
```

To synchronize records

```python3 doplesk_dns_sync/main.py [-h] [-d DOMAIN] command```

```
Synchronize domain DNS records in Plesk with DigitalOcean

positional arguments:
  command     full_sync or single_sync

optional arguments:
  -h, --help  show this help message and exit
  -d DOMAIN   domain to synchronize if single_sync
  ```

*Note: If a domain does not have a DNS zone in Plesk, an empty zone will be created in DigitalOcean*
