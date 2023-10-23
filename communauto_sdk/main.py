from communauto_sdk.client import CommunautoClient
import json

client = CommunautoClient()
# branches = client.getBranches()
# print(type(branches))
# print(branches)
# print(json.dumps(branches, indent=4, ensure_ascii=False))

print(json.dumps(client.getCities(branchId=1), indent=4, ensure_ascii=False))