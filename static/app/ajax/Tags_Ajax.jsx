import axios from 'axios';


export default class Tags_Ajax {
    static checkToken() {
        try {
            sessionStorage.getItem('token')
        } catch (e) {
            if (e instanceof ReferenceError) {
                window.location.href = "/";
            }
        }
    }

    static addTag(tag) {

        Tags_Ajax.checkToken();

        axios({
            method: 'post',
            url: '/api/tags/',
            headers: {'Authorization': 'JWT ' + sessionStorage.getItem('token')},
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
}