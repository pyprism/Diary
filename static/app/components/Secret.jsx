import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import Crypt from '../utils/Crypt.jsx';
import { browserHistory } from 'react-router';


export default class Secret extends React.Component {
    secret(e){
        e.preventDefault();
        let random = Array(8+1).join((Math.random().toString(36)+'00000000000000000').slice(2, 18)).slice(0, 8);
        let secret = ReactDOM.findDOMNode(this.refs.secret).value;

        axios({
            method: 'get',
            url: '/api/secret/',
            headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
        }).then(function (response) {
            console.log(response.data[0].key);
        }).catch(function (response) {
            if(response.status == 404){
                Crypt.encrypt(secret, random).then(function (bunny) {
                    axios({
                        method: 'post',
                        url: '/api/secret/',
                        data: {'key': bunny.data},
                        headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
                    }).then(function(response) {
                        sessionStorage.setItem('key', random);
                        browserHistory.push('/dashboard/stats/');
                    }).catch(function (err) {
                        console.log(err);
                        sweetAlert("Oops!", err, "error");
                    })
                });
            }else if (response.status == 403) {
                browserHistory.push('/');
                sweetAlert("Oops!", 'Token Expired! Login again.', "error");
            }
        });
    }

    render() {
        return (
            <div>
                <form onSubmit={this.secret.bind(this)}>
                    <div className="form-group">
                        <label>Enter Your Secret Key</label>
                        <input type="text" className="form-control" required ref="secret" placeholder="Secret Key" />
                    </div>
                    <button type="submit" className="btn btn-default"><i className="fa fa-bookmark"> Save</i></button>
                </form>
            </div>
        )
    }
}