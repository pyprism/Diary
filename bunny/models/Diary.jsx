import { observable, action, computed, autorun } from 'mobx';
import axios from 'axios';
import Crypt from '../utils/Crypt';
import { toJS } from "mobx";


export class Diary {
    @observable loaded = false;
    @observable searching = false;
    @observable posts = [];
    @observable post = {} ;
    @observable loadingText = 'Loading from remote server....';
    @observable pageId = 0;

    @action getPosts() {
        axios({
            method: 'get',
            url: '/api/diary/',
            headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
        }).then(action('response action', (response) => {
            this.loadingText = 'Decrypting data...';
            (response.data).map(function (post) {
                let salt = forge.util.hexToBytes(post['salt']);
                let key = forge.pkcs5.pbkdf2(sessionStorage.getItem('key'),
                    salt, 100, 16);
                let hiren = {};
                hiren['id'] = post['id'];
                hiren['title'] = Crypt.decrypt(post['title'], key, post['iv']);
                hiren['content'] = Crypt.decrypt(post['content'], key, post['iv']);
                hiren['tag'] = post['tag'];
                hiren['date'] = moment.utc(post['date']).local().format("dddd, DD MMMM YYYY hh:mm:ss A");
                hiren['rawDate'] = post['date'];
                hiren['iv'] = post['iv'];
                hiren['key'] = key;
                hiren['salt'] = salt;
                this.posts.push(hiren);
            }.bind(this));
            this.loaded = true;
        })).catch(function(err) {
            console.error(err);
            sweetAlert("Oops!", err.statusText, "error");
        });
    }

    @action reset() {
        this.loaded = false;
        this.searching = false;
        this.posts = [];
        this.loadingText = 'Loading from remote server....';
    }

    @computed get Data() {
        return this.posts;
    }

    findMe(key) {
        return key.id == this.pageId;
    }

    @action findPostById() {
        this.post =  toJS(this.posts).find(this.findMe.bind(this));
    }


}