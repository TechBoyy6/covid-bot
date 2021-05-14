from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
import random
import requests
import json


app = Flask(__name__)


@app.route("/")
def about():
    return "This is a Whatsapp Bot that extracts the leads from the covid.army api and provide covid resources on whatsapp easily.\nThis initiative its taken by Moiz Rajkotwala\nOnline Portfolio -> moizrajkotwala.netlify.app\nGitHub -> https://github.com/TechBoyy6"

@app.route("/msg", methods=['POST'])
def sms_reply():

    msg = request.form.get('Body')
    s = requests.Session()        

    if msg.lower() == "resources":

        link = "https://api.covid.army/api/resources"
        r = s.get(link)
        res_output = json.loads(r.text)
        gvn = '\n'.join(res_output)
        resp_er = MessagingResponse()
        resp_er.message(gvn)
        return str(resp_er)
        
    else:

        try:
            para = msg.lower().split(" ")
            url="https://api.covid.army/api/tweets/{}/{}".format(para[0], "".join(para[1:]))

            r = s.get(url)
            output = json.loads(r.text)
            rnd_index = random.randint(0, len(output))

            res_type = output[rnd_index]["resource_type"]
            res_num = output[rnd_index]["phone"]
            fi_num = "".join(res_num)
            res_txt = output[rnd_index]["text"]
            user_out = res_type+"\n"+fi_num+"\n"+res_txt
            msg_resp = MessagingResponse()
            msg_resp.message(user_out)
            return str(msg_resp)
        except:
            err_resp = MessagingResponse()
            err_resp.message("Nothing Found :(\nTo imporve the search\n Input correct spelling\nTry different location or resource")
            return str(err_resp)
    


if __name__ == "__main__":
    app.run()
