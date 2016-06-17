/**
 * Created by prism on 4/5/16.
 */
import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, browserHistory, IndexRoute} from 'react-router';
import Login from './components/Login.jsx';
import Dashboard from './components/Dashboard.jsx';
import Tags from './components/Tags.jsx';
import Main from './components/Main.jsx';
import axios from 'axios';
import Secret from './components/Secret.jsx';
import Editor from './components/Editor.jsx';
import Posts from './components/Posts.jsx';


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
            console.log(res);
        }).catch(function(response) {
            replace('/');
            console.log(response);
            sweetAlert("Oops!", 'Token Expired', "info");
        });
    } else {
        replace('/');
    }

}

function keyRequired(nextState, replace){
    if(!sessionStorage.getItem('key')) {
        replace('/dashboard/secret/');
        sweetAlert("Oops!", 'Secret Key Required', "info");
    }
}

ReactDOM.render(
    <Router history={browserHistory} >
        <Route path="/" component={Login} />
        <Route path="/dashboard" onEnter={authRequired} component={Main}>
            <IndexRoute onEnter={keyRequired}  component={Dashboard}/>
            <Route path="stats" onEnter={keyRequired} component={Dashboard} />
            <Route path="secret" component={Secret} />
            <Route path="create" onEnter={keyRequired} component={Editor} />
            <Route path="posts" onEnter={keyRequired}component={Posts} />
            <Route path="tags" onEnter={keyRequired} component={Tags} />
        </Route>

    </Router>,
    document.getElementById('app')
);
