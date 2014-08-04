#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import email
from email.utils import formatdate
from django.conf import settings
from django.core.mail.message import make_msgid
from django.utils.encoding import smart_text
from fetchmyguest.utils.html2plaintext import html2plaintext
import quopri

def prepare_reply(self, message, ):
    """
    Prepares a email reply
    """
    if self.mailbox.from_email:
        message.from_email = self.mailbox.from_email
    else:
        message.from_email = settings.DEFAULT_FROM_EMAIL
    message.extra_headers['Message-ID'] = make_msgid()
    message.extra_headers['Date'] = formatdate()
    message.extra_headers['In-Reply-To'] = self.message_id
    message.extra_headers['References'] = self.message_id
    return message

def reply(self, message, ):
    """Sends a message as a reply to this message instance.

    Although Django's e-mail processing will set both Message-ID
    and Date upon generating the e-mail message, we will not be able
    to retrieve that information through normal channels, so we must
    pre-set it.

    """
    message = self.prepare_reply(message)
    message.send()
    return self.mailbox.record_outgoing_message(
            email.message_from_string(
                message.message().as_string()
            )
        )


def get_text_body(self):
    def get_body_from_message(message):
        body = ''

        def get_plain(part):
            this_charset = part.get_content_charset()
            this_sub_part = part.get_payload(decode=True)
            if this_charset:
                if part.get_content_subtype() == 'html':
                    this_sub_part = html2plaintext(smart_text(quopri.decodestring(this_sub_part),
                                                              encoding=this_charset,
                                                              errors='ignore'),
                                                   encoding='utf-8')
                elif part.get_content_maintype() == 'text':
                    this_sub_part = smart_text(quopri.decodestring(this_sub_part),
                                               encoding=this_charset,
                                               errors='ignore')
            else:
                if part.get_content_subtype() == 'html':
                    this_sub_part = html2plaintext(smart_text(quopri.decodestring(this_sub_part), errors='ignore'),
                                                   encoding='utf-8')
                elif part.get_content_maintype() == 'text':
                    this_sub_part = smart_text(quopri.decodestring(this_sub_part), errors='ignore')
            return this_sub_part.replace("\n\n", "\n").replace("\r\n\r\n", "\r\n")

        for part in message.walk():
            if message.is_multipart():
                if (part.get_content_maintype() == 'text'
                    and part.get_content_subtype() == 'plain'):
                    body += get_plain(part)

            else:
                body += get_plain(part)
        return body
    return get_body_from_message(self.get_email_object()).strip()