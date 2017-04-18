from flask import Flask, request, Response
from marketorestpython.client import MarketoClient
from slackclient import SlackClient
import os

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET','')
MUNCHKIN_ID = os.environ.get('MUNCHKIN_ID','')
MKTO_CLIENT_ID = os.environ.get('MKTO_CLIENT_ID','')
MKTO_CLIENT_SECRET = os.environ.get('MKTO_CLIENT_SECRET','')

availableSwag = {'habitat': 32110}

app = Flask(__name__)

@app.route('/swag', methods=['POST'])
def inbound():
    reply = "Nearly there!"
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        incoming = request.form.get('text').split(" ")
        if len(incoming) > 1:
            reply = processRequest(incoming[0], incoming[1])
        else:
            reply = "You need to say /swag <type> <email>"
    return Response(reply), 200


@app.route('/test', methods=['GET'])
def test():
    return Response('It works!')


def processRequest(swagList, leadName):
    reply = ""

    if swagList in availableSwag:
        listId = availableSwag[swagList]
        mc = MarketoClient(MUNCHKIN_ID, MKTO_CLIENT_ID, MKTO_CLIENT_SECRET)
        lead = mc.execute(method='get_multiple_leads_by_filter_type', filterType='email', filterValues=[leadName], fields=['id', 'firstName','lastName'])
        if len(lead) > 0:
            added = mc.execute(method='add_leads_to_list', listId=29485, id=[lead[0]['id']])
            if(added[0]['status'])=='added':
                reply = "Sending " +swagList +" swag to " + leadName
            else:
                reply = "Couldn't send the swag to this lead. Sorry." 
        else:
            reply = "I can't find that lead in our system. Try again."
    else:
        reply = swagList + " is not a type of swag. Try again."

    return reply

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
