import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, browserHistory, IndexRoute} from 'react-router';
import Login from './components/Login.jsx';
import Dashboard from './components/Dashboard.jsx';
import Main from './components/Main.jsx';
import Form from './components/Form.jsx';
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
            console.log();
        }).catch(function(response) {
            replace('/');
            console.log(response);
            sweetAlert("Oops!", 'Token Expired', "info");
        });
    } else {
        replace('/');
    }

}


ReactDOM.render(
    <Router history={browserHistory} >
        <Route path="/" component={Login} />
        <Route path="/dashboard" onEnter={authRequired} movie={ new Movies() } component={Main}>
            <IndexRoute movie={ new Movies() } component={Dashboard}/>
            <Route path="stats" component={Dashboard} />
            <Route path="movie" component={Movie} />
        </Route>

    </Router>,
    document.getElementById('app')
);