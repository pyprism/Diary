/**
 * Created by prism on 4/5/16.
 */
import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, browserHistory} from 'react-router';
import Login from './components/Login.jsx';
import Dashboard from './components/Dashboard.jsx';
import Tags from './components/Tags.jsx';
import Main from './components/Main.jsx';
import axios from 'axios';
import Secret from './components/Secret.jsx';


function authRequired(nextState, replace) {
    let token = sessionStorage.getItem('token');
    if (token) {
        axios({
            method: 'post',
            url: '/api-token-verify/',
            data: {
                'token': token
            }
        }).catch(function(response) {
            console.log(response);
            replace('/');
        });
    } else {
        replace('/');
    }

}

ReactDOM.render(
    <Router history={browserHistory} >
        <Route path="/" component={Login} />
        <Route path="/dashboard" onEnter={authRequired} component={Main}>
            <Route path="stats" component={Dashboard} />
            <Route path="secret" component={Secret} />
            <Route path="tags" component={Tags} />
        </Route>

    </Router>,
    document.getElementById('app')
);
