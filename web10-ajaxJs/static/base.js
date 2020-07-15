var log = function(){
    console.log.apply(console, arguments)
}

var e = function(sel){
    return document.querySelector(sel)
}

var ajax = function(method, path, data, responseCallback){
    var r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function(){
        if(r.readyState === 4){
            log(r)
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}

var apiTodoAll = function(callback){
    var path = '/api/todo/all'
    ajax('GET', path, '', callback)
}

var apiTodoAdd = function(form, callback){
    var path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

var apiTodoDelete = function(id, callback){
    var path = '/api/todo/delete?id=' + id
    ajax('GET', path, '', callback)
}

var apiTodoUpdate = function(form, callback){
    var path = '/api/todo/update'
    ajax('POST', path, form, callback)
}

var apiWeiboAll = function(callback){
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(form, callback){
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboRemove = function(id, callback){
    var path = '/api/weibo/delete?id=' + id
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback){
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function(form, callback){
    var path = '/api/weibo/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentRemove = function(id, callback){
    var path = '/api/weibo/comment/remove?id=' + id
    ajax('GET', path, '', callback)
}
