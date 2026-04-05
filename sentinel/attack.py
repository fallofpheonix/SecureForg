import urllib.parse

def generate_payloads(plan):
    base = plan["payload_hint"]

    return [
        base,
        urllib.parse.quote(base)
    ]
