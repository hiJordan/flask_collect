/*
1, 给add按钮绑定事件
2，获取input的值
3，构建todo-cell html字符串
4，将todo-cell插入todo-list中
5，给remove按钮绑定事件
*/


//获取页面元素
var e = function(sel){
    return document.querySelector(sel)
}


var todoTemplate = function(todo){
    t = `
        <div class="todo-cell">
            <button class="todo-remove">remove</button>
            <span>${todo}</span>
        </div>
    `

    return t
}


//将todo-cell的值插入html中
var insertTodo = function(todo){
    var todoList = e('.todo-list')
    var todoCell = todoTemplate(todo)
    todoList.insertAdjacentHTML('beforeend', todoCell)
}



//给id为id-button-add的按钮绑定添加todo-cell事件
var b = e('#id-button-add')
b.addEventListener('click', function(){
    var input = e('#id-input-todo')
    var todo = input.value
    insertTodo(todo)
})


//给romove按钮绑定删除事件,测试给单个非浏览器加载时固定按钮绑定按钮
//结果是只作用于加载时存在的html元素。
var todoList = e('.todo-remove')
todoList.addEventListener('click', function(){
    todoList.parentElement.remove()
})
