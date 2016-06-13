import {observable, computed, autorun} from 'mobx';
import axios from "axios";
import crypt from "../utils/Crypt.jsx";

export default class Tags_Ajax {
    static checkToken() {
        try {
            sessionStorage.getItem('token');
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
                'name': tag
            }
        }).then(function (response) {
            if (response.statusText) {
                sweetAlert( response.data.name, response.statusText, "success");
            }
            })
            .catch(function (response) {
                if(response.data.detail) {
                    sweetAlert("Oops!", response.data.detail, "error");
                } else if(response.data.name) {
                    sweetAlert("Oops!", response.data.name[0], "error");
                }
            });
    }
}
//export default class Tag_Store {
//    @observable tags = [];
//}