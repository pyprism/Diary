import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';

export default class Login extends React.Component {

    login(e) {
        e.preventDefault();
        axios({
            method: 'post',
            url: '/api-token-auth/',
            data: {
                'username': ReactDOM.findDOMNode(this.refs.username).value,
                'password': ReactDOM.findDOMNode(this.refs.password).value
            }
        }).then(function (response) {
            if (response.data['token']) {
                sessionStorage.setItem('token', response.data['token']);
                browserHistory.push('/secret/');
            }
        })
            .catch(function (response) {
                sweetAlert("Oops!", 'Username/Password is not correct', "error");
            });
    }
    
    render () {
        return <span>
            <Helmet
                title="Hiren-Diary: Login"
                link={[
                    {"rel": "stylesheet", "href": "/static/css/login.css"},
                    {"rel": "icon", "href": "/static/favicon.ico"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/sweetalert.css"}

                ]}
            />

            <form id="loginform"  onSubmit={this.login.bind(this)} >
                <input type="text" required className="input" autoFocus placeholder="Username" ref="username" />
                <input type="password" required className="input" placeholder="Password" ref="password" />
                <input type="submit" className="loginbutton" value="SIGN IN" />
            </form>

        </span>


    }

}