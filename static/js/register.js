let check_id = 0

function change_id() {
    check_id=0
}


function id_check() {
    var RegExp = /^[a-zA-Z0-9]{4,12}$/;
    var id = document.getElementById("userid");

    // if(id.focus()){
    //     check_id=0;
    // }
    if (id.value == "") {

        id.focus();
        alert("아이디를 입력하세요.");
        return false;
    }
    if (!RegExp.test(id.value)) {
        id.focus();
        alert("ID는 4~12자의 영문 대소문자, 숫자로만 입력해 주세요.");
        return false;
    } else {
        $.ajax({
            type: "POST",
            url: "/api/checkid",
            data: {
                id_give: $('#userid').val(),
            },
            success: function (response) {
                if (response['status'] === 0) {
                    check_id = 1
                    alert('사용 가능한 아이디 입니다.')
                } else {
                    alert('이미 존재하는 아이디 입니다.')
                    id.focus();
                    document.getElementById('userid').value = null
                }
            }
        })

    }
}

function registerform_check() {
    var RegExp = /^[a-zA-Z0-9]{4,12}$/;
    var n_RegExp = /^[a-zA-Z0-9가-힣]{2,8}$/;
    var id = document.getElementById("userid");
    var name = document.getElementById("username");
    var password = document.getElementById("userpw");
    var password2 = document.getElementById("userpw2");

    if (name.value == "") {
        alert("닉네임을 입력하세요.");
        name.focus();
        return false;
    }
    if (!n_RegExp.test(name.value)) {
        name.focus();
        alert("닉네임은 2~8자의 한글, 영문 대소문자, 숫자로만 입력해 주세요.");
        return false;
    }
    if (password.value == "") {
        alert("비밀번호를 입력하세요.");
        password.focus();
        return false;
    } if (!RegExp.test(password.value)) {
        alert("비밀번호는 4~12자의 영문 대소문자, 숫자로만 입력해 주세요.");
        return false;
    } if (password.value == id.value) {
        alert("비밀번호는 ID와 동일하면 안됩니다.");
        return false;
    } if (password.value !== password2.value) {
        alert("비밀번호가 일치하지 않습니다.");
        password2.focus();
        return false;
    } if (check_id===0) {
        alert("아이디를 확인해주세요.")
        return false;
    }
        register();

}

function register() {
    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {
            id_give: $('#userid').val(),
            pw_give: $('#userpw').val(),
            username_give: $('#username').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/login'
            } else {
                alert(response['msg'])
            }
        }
    })
}


//회원가입 중복검사 할 시 필요한 코드 deprecated 됨
// function name_check() {
//     var n_RegExp = /^[a-zA-Z0-9가-힣]{2,8}$/;
//     var name = document.getElementById("username");
//
//
//     if (name.value == "") {
//         alert("닉네임을 입력하세요.");
//         name.focus();
//         return false;
//     }
//
//     if (!n_RegExp.test(name.value)) {
//         name.focus();
//         alert("닉네임은 2~8자의 한글, 영문 대소문자, 숫자로만 입력해 주세요.");
//         return false;
//     } else {
//         $.ajax({
//             type: "POST",
//             url: "/api/checkname",
//             data: {
//                 name_give: $('#username').val(),
//             },
//             success: function (response) {
//                 if (response['status'] === 0) {
//                     check_name = 1
//                     alert('사용 가능한 닉네임 입니다.')
//                 } else {
//                     alert('이미 존재하는 닉네임 입니다.')
//                     name.focus();
//                     document.getElementById('username').value = null
//                 }
//             }
//         })
//
//     }
// }