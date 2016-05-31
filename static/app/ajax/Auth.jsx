import axios from 'axios';

export default class Auth {
    static login(username, password) {
        axios({
            method: 'post',
            url: '/api-token-auth/',
            data: {
                'username': username,
                'password': password
            }
        }).then(function (response) {
            if (response.data['token']) {
                sessionStorage.setItem('token', response.data['token']);
                window.location.href = "/dashboard";
            }
            })
            .catch(function (response) {
                sweetAlert("Oops!", response.data.non_field_errors[0], "error");
            });
    }

    static logout(){
        sessionStorage.removeItem('token');
        window.location.href = "/";
    }
}