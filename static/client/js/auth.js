$('#regist-submit').click(function () {
    var username = $('#username').val();
    var password = $('#password').val();
    var url = $(this).attr('data-url');
    var csrfToken = $('#django-csrf-token').val();

    console.log(username, password, url, csrfToken)
    if (!username || !password) {
        alert('缺少必要字段');
        return;
    }

    $.ajax({
        url: url,
        type: 'post',
        data: {
            username: username,
            password: password,
            csrfmiddlewaretoken: csrfToken
        },
        success: function (data) {
            // console.log(data)
            alert(data.msg);
            // alert('注册成功');

        },
        fail: function (e) {
            // console.log('error:%s', e)
            alert('注册失败');
        }

    })
})



$('#login-submit').click(function () {
    var username = $('#username').val();
    var password = $('#password').val();
    var url = $(this).attr('data-url');
    var csrfToken = $('#django-csrf-token').val();

    console.log(username, password, url, csrfToken)
    if (!username || !password) {
        alert('缺少必要字段');
        return;
    }
    $.ajax({
        url: url,
        type: 'post',
        data: {
            username: username,
            password: password,
            csrfmiddlewaretoken: csrfToken
        },
        success: function (data) {
            alert('登陆成功');

        },
        fail: function (e) {
            alert('注册失败');
        }

    })
})