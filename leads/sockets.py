from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from json import dumps, loads
from agencies.models import Notification
from django import db

from fetchmyguest.utils.redis_utils import get_redis_connection

import logging
logger = logging.getLogger('')

def get_room_chan_name(user=None):
    if user:
        return 'agency{0}_room'.format(user.agent_profile.agency_id)


@namespace('/push')
class NgChatNamespace(BaseNamespace, BroadcastMixin ):
    def initialize(self):
        self.logger = logging.getLogger("socketio.chat")
        self.redis = get_redis_connection()
        self.pubsub = self.redis.pubsub()
        self.listener_greenlet = None

        # self.user = CuserMiddleware.get_user()
        #
        # self.socket.session['user'] = self.user
        # self.environ.setdefault('users', []).append(self.user)
        # self.broadcast_event('announcement', '%s has connected' % self.user)
        # self.broadcast_event('users', self.environ['users'])

        self.emit('connect', 'connected')
        self.log('connected!')

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_subscribe(self, room):
        self.join(room)
        return True, room

    def on_viewed(self, notification_id):
        self.logger.debug(notification_id)
        Notification.objects.get(pk=notification_id).delete()
        self.broadcast_event('deleted', notification_id)
        db.close_connection()

    def join(self, room):
        """
        Kills the existing listener, and starts a new one subscribing to the new channel.
        """
        if getattr(self, 'listener_greenlet', False):
            self.listener_greenlet.kill()

        self.listener_greenlet = self.spawn(self.listener, room)
        self.log("Room {0} joined".format(room))
        self.emit('joined', room)

    def listener(self, room):
        r = get_redis_connection()
        p = r.pubsub()
        p.subscribe(room)
        self.log("Listener started")

        for m in p.listen():
            if m['type'] == 'message':
                data = loads(m['data'])
                # self.emit('pop', 'msg')
                self.emit('alert', data)


    def on_user_message(self, msg):
        self.emit_to_room('main_room', 'msg_to_room', self.socket.session['user'], msg)

    def disconnect(self, silent=False):
        db.close_connection()
        logger.debug('Disconnected')
        super(NgChatNamespace, self).disconnect(silent=silent)