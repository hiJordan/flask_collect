var timeString = function(timestamp){
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

var todoTemplate = function(todo){
    var id = todo.id
    var title = todo.title
    var ut = timeString(todo.ut)
    log('todo', todo)

    var t = `
        <div class="todo-cell" id="todo-${id}" data-id="${id}">
            <button class="todo-edit-button">edit</button>
            <button class="todo-delete-button">remove</button>
            <span class="todo-title">${title}</span>
            <time class="todo-ut">${ut}</time>
        </div>
    `
    return t
}

var insertTodo = function(todo){
    var todo_cell = todoTemplate(todo)
    var todo_list = e('.todo-list')
    todo_list.insertAdjacentHTML('beforeend', todo_cell)

}

var insertEditForm = function(todo_cell){
    var edit_form = `
        <div class="todo-edit-form">
            <input class="todo-edit-input">
            <button class="todo-update-button">update</button>
        </div>
    `
    todo_cell.insertAdjacentHTML('beforeend', edit_form)
}

var loadTodos = function(){
    apiTodoAll(function(r){
        log('end data ', r)
        var todos = JSON.parse(r)

        for(var i=0; i<todos.length; i++)
        {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}

var bindEventTodoAdd = function(){
    var b = e('#id-button-add')
    b.addEventListener('click', function(){
        var input = e('#id-input-todo')
        var title = input.value
        var form = {
            'title': title
        }
        apiTodoAdd(form, function(r){
            var todo = JSON.parse(r)
            insertTodo(todo)
        })
    })
}

var bindEventTodoDelete = function(){
    var todo_list = e('.todo-list')
    todo_list.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('todo-delete-button')){
            var todo_cell = self.parentElement
            var todo_id = todo_cell.dataset.id
            apiTodoDelete(todo_id, function(r){
                log('Removed ', todo_id)
                todo_cell.remove()
            })
        }
    })
}

var bindEventTodoEdit = function(){
    var todo_list = e('.todo-list')
    todo_list.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('todo-edit-button')){
            var todo_cell = self.parentElement
            insertEditForm(todo_cell)
        }
    })

}

var binEventTodoUpdate = function(){
    var todo_list = e('.todo-list')
    todo_list.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('todo-update-button')){
            var edit_form = self.parentElement
            var input = edit_form.querySelector('.todo-edit-input')
            var title = input.value
            var todo_cell = self.closest('.todo-cell')
            var todo_id = todo_cell.dataset.id
            var form = {
                'id': todo_id,
                'title': title,
            }
            apiTodoUpdate(form, function(r){
                log('updated ', todo_id)
                var todo = JSON.parse(r)
                var selector = '#todo-' + todo.id
                var todo_cell = e(selector)
                var todo_span = todo_cell.querySelector('.todo-title')
                log('todo updata', todo, selector, todo_cell, todo_span)
                todo_span.innerHTML = todo.title
            })
        }
    })
}

var bindEvents = function(){
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    binEventTodoUpdate()
}

var __main = function(){
    loadTodos()
    bindEvents()
}

__main()
