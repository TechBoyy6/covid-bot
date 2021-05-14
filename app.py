from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
import random
import requests
import json


app = Flask(__name__)


@app.route("/")
def about():
    abt_msg = """This is a Whatsapp Bot that extracts the leads from the covid.army api and provide covid resources on whatsapp easily.\n
    This initiative is taken by Moiz Rajkotwala\n
    Online Portfolio -> http://moizrajkotwala.netlify.app \n
    GitHub -> https://github.com/TechBoyy6"""
    return abt_msg

@app.route("/msg", methods=['POST'])
def sms_reply():

    msg = request.form.get('Body')
    para = msg.lower().split(" ")
    s = requests.Session()        

    if msg.lower() == "resources" or "resource":

        link = "https://api.covid.army/api/resources"
        r = s.get(link)
        res_output = json.loads(r.text)
        gvn = '\n'.join(res_output)
        res_msg = MessagingResponse()
        res_msg.message(gvn)
        return str(res_msg)
        
    elif len(para) >= 2:

        try:
            
            url="https://api.covid.army/api/tweets/{}/{}".format(para[0], "".join(para[1:]))

            r = s.get(url)
            output = json.loads(r.text)
            rnd_index = random.randint(0, len(output))

            res_type = output[rnd_index]["resource_type"]
            res_num = output[rnd_index]["phone"]
            fi_num = "".join(res_num)
            res_txt = output[rnd_index]["text"]
            user_out = res_type+"\n"+fi_num+"\n"+res_txt
            main_msg = MessagingResponse()
            main_msg.message(user_out)
            return str(main_msg)
        except:
            err_msg = MessagingResponse()
            err_msg.message("Nothing Found :(\nTo imporve the search\n Input correct spelling\nTry different location or resource")
            return str(err_msg)
        
    else:
        intro = """Hello, Myself 'Covid Resource Bot'\n
                    *Type 'resources' to know the list of resources you can search for.\n
                    *Type 'Location<space>Resource' to get lead message.
                    example -> mumbai oxygen"""
        
        intro_msg = MessagingResponse()
        intro_msg.message(intro)
        return str(intro_msg)
    


if __name__ == "__main__":
    app.run()
