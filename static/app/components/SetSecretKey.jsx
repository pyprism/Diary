import React from 'react';
import ReactDOM from 'react-dom';

export default class SetSecretKey extends React.Component {
    newTag(e){
        e.preventDefault();
        sessionStorage.setItem('key', ReactDOM.findDOMNode(this.refs.secret).value);
        ReactDOM.findDOMNode(this.refs.secret).value = "";  // clear field
    }

    render() {
        return (
            <div>
                <form onSubmit={this.newTag.bind(this)}>
                    <div className="form-group">
                        <label>Your Secret Key</label>
                        <input type="text" className="form-control" required ref="secret" placeholder="Secret Key" />
                    </div>
                    <button type="submit" className="btn btn-default"><i className="fa fa-bookmark"> Save</i></button>
                </form>
            </div>
        )
    }
}