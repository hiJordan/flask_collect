var timeString = function(timestamp){
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

var commenTemplates = function(comments){
    var html = ''
    for(var i = 0; i < comments.length; i++){
        var comment = comments[i]
        var id = comment.id
        var t = `
            <div id="comment-${id}" data-comment_id="${id}">
                ${comment.content}
                <button class="comment-remove-button">remove</button>
            </div>
        `
        html += t
    }
    return html
}

var weiboTemplate = function(weibo){
    var id = weibo.id
    var content = weibo.content
    var comments = commenTemplates(weibo.comments)

    var t = `
        <br />
        <div class="weibo-cell" id="weibo-${id}" data-id="${id}">
            <div class="weibo-body">
                <button class="weibo-edit-button">edit</button>
                <button class="weibo-delete-button">remove</button>
                <span class="weibo-content-span">${content}</span>
            </div>
            <div class="comment-list">
                ${comments}
            </div>
            <div class="comment-form" data-weibo_id="${id}">
                <input class="input-add-comment">
                <br />
                <button class="comment-add">add comment</button>
            </div>
        </div>
    `
    return t
}

var insertWeibo = function(weibo){
    var weibo_cell = weiboTemplate(weibo)
    var weibo_list = e('.weibo-list')
    weibo_list.insertAdjacentHTML('beforeend', weibo_cell)
}

var insertComment = function(comment){
    var array_comment = Array(comment)
    var content = commenTemplates(array_comment)
    var selector = '#weibo-' + comment.weibo_id
    var weibo_cell = e(selector)
    var comment_list = weibo_cell.querySelector('.comment-list')
    comment_list.insertAdjacentHTML('beforeend', content)
}

var insertEditForm = function(weibo_body){
    var edit_form = `
        <div class="weibo-edit-form">
            <input class="weibo-edit-input">
            <button class="weibo-update-button">update</button>
        </div>
    `
    weibo_body.insertAdjacentHTML('beforeend', edit_form)
}

var loadWeibos = function(){
    apiWeiboAll(function(r){
        var weibos = JSON.parse(r)
        log('weibos:', weibos)
        for(var i=0; i<weibos.length; i++)
        {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
}

var bindEventWeiboAdd = function(){
    var b = e('#id-button-add-weibo')
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        var form = {
            'content': content
        }
        apiWeiboAdd(form, function(r){
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}

var bindEventWeiboDelete = function(){
    var weibo_list = e('.weibo-list')
    weibo_list.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('weibo-delete-button')){
            var weibo_cell = self.closest('.weibo-cell')
            var weibo_id = weibo_cell.dataset.id
            log('weibo_id:', weibo_id)
            apiWeiboRemove(weibo_id, function(r){
                log('Removed ', weibo_id)
                weibo_cell.remove()
            })
        }
    })
}

var bindEventWeiboEdit = function(){
    var weibo_list = e('.weibo-list')
    weibo_list.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('weibo-edit-button')){
            var weibo_body = self.parentElement
            insertEditForm(weibo_body)
        }
    })

}

var bindEventWeiboUpdate = function(){
    var weibo_list = e('.weibo-list')
    weibo_list.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('weibo-update-button')){
            var edit_form = self.parentElement
            var input = edit_form.querySelector('.weibo-edit-input')
            var content = input.value
            var weibo_cell = self.closest('.weibo-cell')
            var weibo_id = weibo_cell.dataset.id
            var form = {
                'id': weibo_id,
                'content': content,
            }
            apiWeiboUpdate(form, function(r){
                log('updated ', weibo_id)
                var weibo = JSON.parse(r)
                var selector = '#weibo-' + weibo.id
                var weibo_cell = e(selector)
                var weibo_span = weibo_cell.querySelector('.weibo-content-span')
                log('weibo updata', weibo, selector, weibo_cell, weibo_span)
                weibo_span.innerHTML = weibo.content
            })
        }
    })
}

var bindEventCommentAdd = function(){
    var b = e('.weibo-list')
    b.addEventListener('click', function(event){
        self = event.target
        if(self.classList.contains('comment-add')){
            comment_form = self.parentElement
            var weibo_id = comment_form.dataset.weibo_id
            var input = comment_form.querySelector('.input-add-comment')
            var content = input.value
            var form = {
                'weibo_id': weibo_id,
                'content': content
            }
            log('form: ', form)
            apiCommentAdd(form, function(r){
                var comment = JSON.parse(r)
                log('response: ', comment)
                insertComment(comment)
            })
        }
    })
}

var bindEventCommentRemove = function(){
    var weibo_list = e('.weibo-list')
    weibo_list.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('comment-remove-button')){
            var comment_cell = self.parentElement
            var comment_id = comment_cell.dataset.comment_id
            log('weibo_id:', comment_id)
            apiCommentRemove(comment_id, function(r){
                log('Removed ', comment_id)
                comment_cell.remove()
            })
        }
    })
}

var bindEvents = function(){
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()
    bindEventCommentRemove()
}

var __main = function(){
    loadWeibos()
    bindEvents()
}

__main()
