import React from 'react';
import ReactDOM from 'react-dom';

export default class GetSecretKey extends React.Component {

    newKey(e){
        e.preventDefault();
        sessionStorage.setItem('key', ReactDOM.findDOMNode(this.refs.secret).value);
    }

    showKey(e) {
        e.preventDefault();
        ReactDOM.findDOMNode(this.refs.secret).type = 'text';
    }

    render() {
        return (
            <div>
                <form onSubmit={this.newKey.bind(this)}>
                    <div className="form-group">
                        <label>Your Secret Key</label>
                        <input type="password" className="form-control" required ref="secret" onChange={ this.newKey.bind(this) } defaultValue={ sessionStorage.getItem('key')} />
                    </div>
                    <button type="submit" className="btn btn-default"><i className="fa fa-key"> Change Key</i></button>
                    <button type="button" className="btn btn-default" ><i className="fa fa-unlock"> Show Key</i></button>
                </form>
            </div>
        )
    }
}