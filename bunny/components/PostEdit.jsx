import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';
import Crypt from '../utils/Crypt';
import { toJS } from "mobx";



export default class PostEdit extends React.Component {

    form(e) {
        /***
         * Handle post update
         */
        e.preventDefault();

        let  random = this.props.route.posts.post['iv'],
            key = this.props.route.posts.post['key'],
            _id = this.props.route.posts.pageId,
            salt = forge.util.bytesToHex(this.props.route.posts.post['salt']);

        axios({
            method: 'put',
            url: '/api/diary/' + _id + '/',
            data: {
                'tag' : this.props.route.posts.post['tag'],
                'title': Crypt.encrypt(ReactDOM.findDOMNode(this.refs.title).value, key, random),
                'content': Crypt.encrypt(ReactDOM.findDOMNode(this.refs.content).value, key, random),
                'iv': forge.util.bytesToHex(random),
                'salt': salt,
                'date': ReactDOM.findDOMNode(this.refs.date).value
            },
            headers: {
                'Authorization': "JWT " + sessionStorage.getItem('token')
            }
        }).then(function (response) {
            if(response.statusText === "OK") {
                sweetAlert("Updated", "Updated Successfully", "success");
                browserHistory.push('/dashboard/posts/');
            }
        }).catch(function (error) {
            if(error.statusText === 'Forbidden') {
                sweetAlert("Oops!", 'Token Expired, Log Out Plz !', "error");
            }
            sweetAlert('Error', error.statusText, 'error');
        })
    }

    componentDidMount() {
        $('#summernote').summernote({  // initializer for summernote
            height: 150
        });


        $('#datetimepicker').datetimepicker({  // initializer for datetimepicker
            format: 'YYYY-MM-D H:mm:ss'
        });
    }

    render() {

        return (
            <div >
                <div className="row">
                    <Helmet
                        title="Hiren-Diary: Edit Post"
                    />
                </div>

                <form className="form-horizontal" onSubmit={this.form.bind(this)}>
                    <div className="form-group" id="title">
                        <label className="control-label col-sm-2" >Title</label>
                        <div className="col-sm-10">
                            <input type="text" className="form-control" defaultValue={this.props.route.posts.post['title']} ref="title" placeholder="Post Title"/>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="control-label col-sm-2" >Content</label>
                        <div className="col-sm-10">
                            <textarea id="summernote" defaultValue={this.props.route.posts.post['content']} ref="content" className="form-control" placeholder="Enter Content"/>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="control-label col-sm-2">Date</label>
                        <div className='input-group date' id='datetimepicker'>
                            <input type='text' defaultValue={this.props.route.posts.post['rawDate']} ref="date" className="form-control" />
                                    <span className="input-group-addon">
                                        <span className="glyphicon glyphicon-calendar" />
                                    </span>
                        </div>
                    </div>
                    <div className="form-group">
                        <div className="col-sm-offset-2 col-sm-10">
                            <button type="submit" className="btn btn-default"><i className="fa fa-save" /> Update</button>
                        </div>
                    </div>
                </form>
            </div>
        )
    }

}