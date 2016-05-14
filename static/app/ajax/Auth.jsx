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
            sessionStorage.setItem('token', response.data['token']);
            window.location.href = "/dashboard";
            })
            .catch(function (response) {
                console.error(response);
            });
    }

    static logout(){
        sessionStorage.removeItem('token');
        window.location.href = "/";
    }
}