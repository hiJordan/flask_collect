/*
1，给登录绑定检测事件
2，第一位是字母且长度最小为2
3，若符合规则则Log
*/


var log = function(){
    console.log.apply(console, arguments)
}


var e = function(sel){
    return document.querySelector(sel)
}


var check_uname = function(uname){
    first_reg = /^[A-Za-z]/
    end_reg = /[A-Za-z0-9]$/
    all_reg = /^[A-Za-z0-9_]+$/
    cl_uname = uname.length >= 2 && uname.length <=10
    reg_unmae = first_reg.test(uname[0]) && end_reg.test(uname[uname.length-1])
    check = reg_unmae && cl_uname && all_reg.test(uname)
    return check
}


var flash_template = function(flash){
    tip = `
        <h3>${flash}</h3>
    `
    return tip
}


var b_login = e('#id-button-login')
b_login.addEventListener('click', function(){
    todo_login = e('.todo-login')
    input_uname = e('#id-input-uname').value
    if(check_uname(input_uname)){
        tip = e('#id-h3-tip')
        tip.innerText = '检查合格'
    }
    else{
        input_uname = e('#id-input-uname')
        input_uname.value = null
        tip = e('#id-h3-tip')
        tip.innerText = '用户名错误'

    }
})
