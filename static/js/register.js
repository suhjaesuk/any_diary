let check_id = 0

function change_id() {
    check_id=0
}
function id_check() {
    var RegExp = /^[a-zA-Z0-9]{4,12}$/; //

    var id = document.getElementById("userid");
    if (id.value == "") {
        alert("아이디를 입력하세요.");

        return false;
    }
    if (!RegExp.test(id.value)) {
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
                    document.getElementById('userid').value = null
                }
            }
        })

    }
}




function registerform_check() {

    //검사 변수
    var RegExp = /^[a-zA-Z0-9]{4,12}$/; //
    var n_RegExp = /^[a-zA-Z0-9가-힣]{2,8}$/; //닉네임 유효성 검사
    //변수에 담아주기

    var id = document.getElementById("userid");
    var nickname = document.getElementById("usernick");
    var password = document.getElementById("userpw");
    var password2 = document.getElementById("userpw2");


     if (nickname.value == "") {
        alert("닉네임을 입력하세요.");
        nickname.focus();
        return false;
    } else if (!n_RegExp.test(nickname.value)) {
        alert("닉네임은 2~8자의 한글, 영문 대소문자, 숫자로만 입력해 주세요.");
        nickname.focus();
        return false;
    } else if (password.value == "") {
        alert("비밀번호를 입력하세요.");
        password.focus();
        return false;
    } else if (!RegExp.test(password.value)) {
        alert("비밀번호는 4~12자의 영문 대소문자, 숫자로만 입력해 주세요.");
        return false;
    } else if (password.value == id.value) {
        alert("비밀번호는 ID와 동일하면 안됩니다.");
        return false;
    } else if (password.value !== password2.value) {
        alert("비밀번호가 일치하지 않습니다.");
        password2.focus();
        return false;
    } else if (check_id===0) {
        alert("아이디를 확인해주세요.")
        return false;

    }
    else {
        register();
    }
}

function register() {
    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {
            id_give: $('#userid').val(),
            pw_give: $('#userpw').val(),
            nickname_give: $('#usernick').val()
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