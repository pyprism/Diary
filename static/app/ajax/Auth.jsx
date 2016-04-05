import $ from 'jquery';

export default class Auth {
    static login(username, password) {
        $.ajax({
            method: 'POST',
            url: '/api-token-auth/',
            data: {'username': username, 'password': password},
            success: function(response) {
                if(response.token) {
                    sessionStorage.setItem('token', response.token);
                    window.location.href = "/dashboard";
                }
            },
            error: function(jqXHR, exception) {
                alert(jqXHR.responseText);
            }
        });
    }

    static logout(){
        sessionStorage.removeItem('token');
        window.location.href = "/";
    }
}