import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, browserHistory, IndexRoute} from 'react-router';
import Login from './components/Login.jsx';
import Posts from './components/Posts.jsx';
import Main from './components/Main.jsx';
import Secret from './components/Secret.jsx';
import Form from './components/Form.jsx';
import Notes from './components/Notes.jsx';
import axios from 'axios';
//import { Movies } from './models/Movies.jsx';

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


ReactDOM.render(
    <Router history={browserHistory} >
        <Route path="/" component={Login} />
        <Route path="/secret" component={Secret} />
        <Route path="/dashboard" onEnter={authRequired} component={Main}>
            <IndexRoute component={Posts}/>
            <Route path="posts" component={Posts} />
            <Route path="new" component={Form} />
            <Route path="notes" component={Notes} />
        </Route>

    </Router>,
    document.getElementById('app')
);