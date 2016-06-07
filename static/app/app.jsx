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



/*
ReactDOM.render(
    <Router history={browserHistory} >
        <Route path="/" component={Login}> </Route>
        <Route path="/dashboard" component={Dashboard}> </Route>
        <Route path="/dashboard/tags" component={Tags}> </Route>
    </Router>,
    document.getElementById('app')
);
*/

ReactDOM.render(
    <Router history={browserHistory} >
        <Route path="/" component={Login}> </Route>
        <Route path="/dashboard" component={Main}>
            <Route path="stats" component={Dashboard} />
            <Route path="tags" component={Tags} />
        </Route>

    </Router>,
    document.getElementById('app')
);