import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';


export default class Secret extends React.Component {

    secret(e) {
        e.preventDefault();
        sessionStorage.setItem('key', ReactDOM.findDOMNode(this.refs.secret).value);
        browserHistory.push('/dashboard/posts/');
    }

    render () {
        return <span>
            <Helmet
                title="Hiren-Diary: Secret Key"
                link={[
                    {"rel": "stylesheet", "href": "/static/css/login.css"},
                    {"rel": "icon", "href": "/static/favicon.ico"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/sweetalert.css"}
                ]}
            />

            <form id="loginform"  onSubmit={this.secret.bind(this)} >
                <input type="password" required className="input" autoFocus placeholder="Secret Key" ref="secret" />
                <input type="submit" className="loginbutton" value="Proceed" />
            </form>

        </span>


    }

}