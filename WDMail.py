# WANdisco Mail module
#
# Version 16.8.3
#
# Author: Peter Pakos <peter.pakos@wandisco.com>

from __future__ import print_function
import sendgrid
import urllib2
import os


class WDMail(object):
    def __init__(self, api_key):
        os.environ['SENDGRID_API_KEY'] = api_key
        self._sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

    def send(self, sender, recipients, subject, message, html=False, cc=None):
        content = ''
        content_type = 'text/plain'
        if html:
            content_type = 'text/html'
            content += '''
<html>
<body>
<pre>
'''
        content += message

        if html:
            content += '''
</pre>
</body>
</html>
'''
        recipient_list = []
        for recipient in recipients:
            recipient_list.append({"email": recipient})
        data = {
            'personalizations': [
                {
                    'to': recipient_list,
                    'subject': subject
                }
            ],
            'from': {
                'email': sender
            },
            'content': [
                {
                    'type': content_type,
                    'value': content
                }
            ]
        }
        if cc is not None:
            cc_list = []
            for c in cc:
                cc_list.append({'email': c})
            data['personalizations'][0]['cc'] = cc_list
        response = None
        try:
            response = self._sg.client.mail.send.post(request_body=data)
        except urllib2.HTTPError as err:
            print(err)
            exit(1)

        return response.status_code
