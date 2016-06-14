import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
//import Crypt from '../utils/Crypt.jsx';
import { browserHistory } from 'react-router';


export default class Secret extends React.Component {
    secret(e){
        e.preventDefault();
        let random = Array(8+1).join((Math.random().toString(36)+'00000000000000000').slice(2, 18)).slice(0, 8);
        let secret = ReactDOM.findDOMNode(this.refs.secret).value;
        //sessionStorage.setItem('key', ReactDOM.findDOMNode(this.refs.secret).value);
        //ReactDOM.findDOMNode(this.refs.secret).value = "";  // clear field
        axios({
            method: 'get',
            url: '/api/secret/1/',
            headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
        }).then(function (response) {
            console.log(response);
            console.log('hitti');
        }).catch(function (response) {
            if(response.status == 404){
                // axios({
                //     method: 'post',
                //     url: '/api/secret/',
                //     data: {'key': Crypt.encrypt(ReactDOM.findDOMNode(this.refs.secret).value, random)},
                //     headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
                // }).then(function(response) {
                //     console.table(response);
                // })
                console.log('1 hit');
                //console.log(Crypt.encrypt(ReactDOM.findDOMNode(this.refs.secret).value, random));
               // console.log(Crypt.encrypt('x', random));
                console.log('2 hit');
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
                        <label>Enter Your Encryption Key</label>
                        <input type="text" className="form-control" required ref="secret" placeholder="Encryption Key" />
                    </div>
                    <button type="submit" className="btn btn-default"><i className="fa fa-bookmark"> Save</i></button>
                </form>
            </div>
        )
    }
}