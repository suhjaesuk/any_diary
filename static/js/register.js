function registerform_check() {
    //검사 변수
    var RegExp = /^[a-zA-Z0-9]{4,12}$/; //
    var n_RegExp = /^[a-zA-Z0-9가-힣]{2,8}$/; //닉네임 유효성 검사
    //변수에 담아주기

    var id = document.getElementById("userid");
    var nickname = document.getElementById("usernick");
    var password = document.getElementById("userpw");
    var password2 = document.getElementById("userpw2");

    if (id.value == "") { //해당 입력값이 없을 경우 같은말: if(!id.value)
        alert("아이디를 입력하세요.");
        id.focus(); //focus(): 커서가 깜빡이는 현상, blur(): 커서가 사라지는 현상
        return false; //return: 반환하다 return false:  아무것도 반환하지 말아라 아래 코드부터 아무것도 진행하지 말것
    } else if (!RegExp.test(id.value)) { //아이디 유효성검사
        alert("ID는 4~12자의 영문 대소문자, 숫자로만 입력해 주세요.");
        return false;
    } else if (nickname.value == "") { //해당 입력값이 없을 경우 같은말: if(!id.value)
        alert("닉네임을 입력하세요.");
        nickname.focus(); //focus(): 커서가 깜빡이는 현상, blur(): 커서가 사라지는 현상
        return false; //return: 반환하다 return false:  아무것도 반환하지 말아라 아래 코드부터 아무것도 진행하지 말것
    } else if (!n_RegExp.test(nickname.value)) { //아이디 유효성검사
        alert("닉네임은 2~8자의 한글, 영문 대소문자, 숫자로만 입력해 주세요.");
        nickname.focus();
        return false;
    } else if (password.value == "") {
        alert("비밀번호를 입력하세요.");
        password.focus();
        return false;
    } else if (!RegExp.test(password.value)) { //패스워드 유효성검사
        alert("비밀번호는 4~12자의 영문 대소문자, 숫자로만 입력해 주세요.");
        return false;
    } else if (password.value == id.value) { //패스워드와 ID가 동일한지 검사
        alert("비밀번호는 ID와 동일하면 안됩니다.");
        return false;
    } else if (password.value !== password2.value) {
        alert("비밀번호가 일치하지 않습니다.");
        password2.focus();
        return false;
    } else {
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