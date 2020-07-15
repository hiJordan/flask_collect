from flask import session
from flask_socketio import join_room, leave_room, emit
from .. import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = message.get('msg', '')
    session['room'] = room
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    print('text room: ', session['room'], message)
    room = message.get('room')
    emit('message', {'msg': session.get('name') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    session.pop('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
