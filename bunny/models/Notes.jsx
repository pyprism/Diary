import { observable, action, computed, autorun } from 'mobx';
import axios from 'axios';
import Crypt from '../utils/Crypt';
import { toJS } from "mobx";


export class Notes {
    @observable loaded = false;
    @observable searching = false;
    @observable notes = [];
    @observable note = {} ;
    @observable loadingText = 'Loading from remote server....';
    @observable noteId = 0;

    @action getNotes() {
        this.notes = [];
        axios({
            method: 'get',
            url: '/api/notes/',
            headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
        }).then(action('response action', (response) =>{
            this.loadingText = 'Decrypting data...';
            (response.data).map(function (note) {
                let salt = forge.util.hexToBytes(note['salt']);
                let key = forge.pkcs5.pbkdf2(sessionStorage.getItem('key'),
                    salt, 1500, 32);
                let hiren = {};
                hiren['id'] = note['id'];
                hiren['content'] = Crypt.decrypt(note['content'], key, note['iv']);
                hiren['tag'] = note['tag'];
                hiren['date'] = moment.utc(note['date']).local().format("dddd, DD MMMM YYYY hh:mm:ss A");
                hiren['rawDate'] = note['date'];
                hiren['iv'] = note['iv'];
                hiren['key'] = key;
                hiren['salt'] = salt;
                this.notes.push(hiren);
            }.bind(this));
            this.loaded = true;
        })).catch(function (error) {
            console.error(error);
            sweetAlert("Oops!", error.statusText, "error");
        })
    }

    findMe(key) {
        return key.id == this.noteId;
    }

    @action findNoteById() {
        this.loaded = true;
        this.note =  toJS(this.notes).find(this.findMe.bind(this));
    }
}