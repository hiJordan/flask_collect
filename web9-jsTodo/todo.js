/*
1, 给add button绑定事件
2, 在事件处理函数中，获取Input值
3, 用获取的值组装一个todo-cell html字符串
4, 插入todo-list中
*/


//信息输出
var log = function(){
    console.log.apply(console, arguments)
}

//元素查找
var e = function(sel){
    return document.querySelector(sel)
}

//todo-cell元素构建
var todoTemplate = function(todo){
    var t = `
        <div class="todo-cell">
            <button class="todo-remove">remove</button>
            <span>${todo}</span>
        </div>
    `
    return t
}

//将构建的todo-cell内容插入到class为todo-list的div中
var insertTodo = function(todo){
    var todoCell = todoTemplate(todo)
    var todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

//在add按钮中绑定元素添加事件
var b = e('#id-button-add')
b.addEventListener('click', function(){
    log('click')
    var input = e('#id-input-todo')
    var todo = input.value
    insertTodo(todo)
})

//在remove中绑定是删除事件
var todoList = e('.todo-list')
todoList.addEventListener('click', function(event){
    //function中默认有event参数，其值包含被触发事件的所有信息
    //可通过log(event)打印其,event.target得到被点击的元素
    //log('click todolist:', evnet)
    var self = event.target
    log('clicked', self)
    //元素的classList中包含元素的所有class
    if(self.classList.contains('todo-remove')){
        log('click removed')
        self.parentElement.remove()
    }
    else{
        //
    }
})
