from cmath import exp
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dateutil import parser as date_parse

import json

credential = DefaultAzureCredential(
    exclude_cli_credential=True,
    exclude_environment_credential=True,
    exclude_managed_identity_credential=True,
    exclude_powershell_credential=True,
    exclude_visual_studio_code_credential=True,
    exclude_shared_token_cache_credential=True,
    exclude_interactive_browser_credential=False
)
try:
    keyvault_url = input("Keyvault URL: ")
    json_file = "./secrets.json"
    secret_client = SecretClient(vault_url=keyvault_url, credential=credential)


    with open(json_file, 'r') as secret_in_bulk:
        contents = json.loads(secret_in_bulk.read())
        for secret in contents:  
            try: 
                expires_on = date_parse.parse(
                    secret['expires_on']
                )
            except KeyError:
                expires_on = None

            secret_client.set_secret(
                name=secret['name'],
                value=secret['content'],
                enabled=True,
                content_type=secret['description'],
                expires_on=expires_on
            )
except KeyboardInterrupt:
    print("")
    print("Cancelled...")