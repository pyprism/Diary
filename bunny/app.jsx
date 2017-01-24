import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, browserHistory, IndexRoute} from 'react-router';
import Login from './components/Login.jsx';
import Posts from './components/Posts.jsx';
import Post from './components/Post.jsx';
import PostEdit from './components/PostEdit.jsx';
import Main from './components/Main.jsx';
import Secret from './components/Secret.jsx';
import Form from './components/Form.jsx';
import Notes from './components/Notes.jsx';
import NoteEdit from './components/NoteEdit.jsx';
import {Notes as NotesStore} from './models/Notes.jsx';
import axios from 'axios';
import { Diary } from './models/Diary.jsx';

function authRequired(nextState, replace) {
    let token = sessionStorage.getItem('token');
    if (token) {
        axios({
            method: 'post',
            url: '/api-token-verify/',
            data: {
                'token': token
            }
        }).then(function (res) {

        }).catch(function(response) {
            replace('/');
            sweetAlert("Oops!", 'Token Expired', "info");
        });
    } else {
        replace('/');
    }

}

var diary = new Diary();
var notes = new NotesStore();

ReactDOM.render(
    <Router history={browserHistory} >
        <Route path="/" component={Login} />
        <Route path="/secret" component={Secret} />
        <Route path="/dashboard" onEnter={authRequired} component={Main}>
            <IndexRoute posts={ diary } component={Posts}/>
            <Route path="posts" posts={ diary } component={Posts} />
            <Route path="posts/:id/" posts={ diary } component={Post} />
            <Route path="posts/:id/edit" posts={ diary } component={PostEdit} />
            <Route path="new" component={Form} />
            <Route path="notes" notes={notes} component={Notes} />
            <Route path="notes/:id/" notes={notes} component={NoteEdit} />
        </Route>

    </Router>,
    document.getElementById('app')
);