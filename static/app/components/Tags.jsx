import React from 'react';
import Tag_Ajax from "../store/Tag_Store.jsx";
import ReactDOM from 'react-dom';


export default class Tags extends React.Component {

    newTag(e){
        e.preventDefault();
        Tag_Ajax.addTag(ReactDOM.findDOMNode(this.refs.new_tag).value);
        ReactDOM.findDOMNode(this.refs.new_tag).value = "";  // clear field 
    }

    render() {
        return (
            <div>
                <form onSubmit={this.newTag.bind(this)}>
                    <div className="form-group">
                        <label>Create New Tag</label>
                        <input type="text" className="form-control" required ref="new_tag" placeholder="New Tag Name" />
                    </div>
                    <button type="submit" className="btn btn-default"><i className="fa fa-bookmark"> Save</i></button>
                </form>
            </div>
        )
    }
}