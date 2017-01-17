import { observable, action, computed, autorun } from 'mobx';
import axios from 'axios';
import Crypt from '../utils/Crypt';

export class Diary {
    @observable loaded = false;
    @observable posts = [];
    @observable loadingText = 'Loading from remote server....';

    @action getPosts() {
        axios({
            method: 'get',
            url: '/api/diary/',
            headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
        }).then(action('response action', (response) => {
            this.loadingText = 'Decrypting data...';
            (response.data).map(function (post) {
                let key = forge.pkcs5.pbkdf2(sessionStorage.getItem('key'),
                    forge.util.hexToBytes(post['salt']), 100, 16);
                let hiren = [];
                hiren['id'] = post['id'];
                hiren['title'] = Crypt.decrypt(post['title'], key, post['iv']);
                hiren['content'] = Crypt.decrypt(post['content'], key, post['iv']);
                hiren['tag'] = post['tag'];
                hiren['date'] = moment.utc(post['date']).local().format("dddd, DD MMMM YYYY hh:mm:ss A");
                this.posts.push.apply(this.posts, hiren);
            }.bind(this));
            this.loaded = true;
        })).catch(function(err) {
            console.error(err);
          sweetAlert("Oops!", err.statusText, "error");
        });
    }

    @computed get Data() {
        return this.posts;
    }
}