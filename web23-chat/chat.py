"""
1.页面切分：
    1.1 index页, 输入用户名称进入，<input>
    1.2 chat页， 用于在不同房间中聊天， <a>--房间水平列表链接， <textarea>--聊天窗口， <input>聊天信息输入
        1.2.1 socketio在客户端的设置
        --var socket, current_channel
        --function:
            change_channel() --> doc.title=channel current_channel-->id-div-channel-title
            clear_board() --> id-chat-area-->val('')
            $(document).ready() --> socket=io.connect socket.on('connect', )
                change_channel() socket.on('status') socket.on('message')
                keypress() --> keyCode == 13(Enter) --> current_channel is null -->禁止加入
                           --> get #text.val() --> clear #text --> socket.emit('text')
                .rc-channel --> click --> current_channel is not null --> emit('left')
                            --> change_channel clear_board --> emit('joined')
2.逻辑
    2.1 index页<-->index路由， 先判断请求类别，get渲染显示index页面，post验证name数据，存于session中，重定向到chat页
    2.2 chat页<-->chat路由, 判断name是否存在，存在则渲染，反之redirect到index
        2.2.1 flask_socketio in server
        --joined() --> room=message['msg'] --> emit('status')
        --text() --> room --> emit('message')
        --left() --> room --> leave_room(room) --> emit('status')
"""

from app import create_app, socketio

app = create_app(debug=True)

if __name__ == "__main__":
    socketio.run(app)
