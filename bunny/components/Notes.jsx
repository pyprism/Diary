import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';
import { observer } from "mobx-react";
import {Link} from 'react-router';
import Crypt from '../utils/Crypt';
//import NoteEdit from "./NoteEdit.jsx";


@observer
export default class Notes extends React.Component {

    componentDidMount() {
        this.props.route.notes.getNotes();
    }

    fullNote(){
        $('#noteFull').modal();
    }

    editor(){
        $('#noteEdit').modal();
        $('#editNote').summernote({  // initializer for summernote
            height: 150
        });
        $('#datetimepicker').datetimepicker({  // initializer for datetimepicker
            format: 'YYYY-MM-D H:mm:ss'
        });
    }

    form(e) {  //not working !
        /***
         * Handle post update
         */
        e.preventDefault();

        let random = ReactDOM.findDOMNode(this.refs.iv).value,
            key = ReactDOM.findDOMNode(this.refs.key).value,
            _id = ReactDOM.findDOMNode(this.refs.id).value;
        console.log(ReactDOM.findDOMNode(this.refs.content).value);
        axios({
            method: 'patch',
            url: '/api/notes/' + _id + '/',
            data: {
                'content': Crypt.encrypt(ReactDOM.findDOMNode(this.refs.content).value, key, random)
            },
            headers: {
                'Authorization': "JWT " + sessionStorage.getItem('token')
            }
        }).then(function (response) {
            if(response.statusText === "OK") {
                sweetAlert("Updated", "Note updated", "success");
                browserHistory.push('/dashboard/posts/');
            }
        }).catch(function (error) {
            if(error.statusText === 'Forbidden') {
                sweetAlert("Oops!", 'Token Expired, Log Out Plz !', "error");
            }
            sweetAlert('Error', error.statusText, 'error');
        })
    }

    deleteNote(id){
        let message = "Delete the note.",
            title = "Are you sure ?";
        eModal.confirm(message, title)
            .then(function(){
                axios({
                    method: 'delete',
                    url: '/api/notes/' + id + '/',
                    headers: {
                        'Authorization': "JWT " + sessionStorage.getItem('token')
                    }
                }).then(function (data) {
                    sweetAlert("Deleted", "Note deleted", "success");
                    browserHistory.push('/dashboard/posts/');
                }).catch(function (error) {
                    sweetAlert("Error", "Error in deletion!", "error");
                })
            }, function(){

            });
    }

    bunny(){
        return (this.props.route.notes.notes).map((data, index) => {
            return (
                <div className="col-md-5" key={ data.id }>
                    <div className="card-wrapper" >
                        <div className="card">
                            <p dangerouslySetInnerHTML={{__html: data['content']}} className="desc-text text-justify">
                            </p>
                            <ul className="controls">
                                <li className="read">
                                    <p className="text-a" onClick={() => this.fullNote(data)} >
                                        <i className="fa fa-arrows-alt"/> Read Full</p>
                                </li>

                                <li className="views">
                                    <p className="text-a" >
                                        <i className="fa fa-edit"/> Edit</p>
                                </li>
                                <li className="comment">
                                    <p className="text-a" onClick={() => this.deleteNote(data.id)} > <i className="fa fa-remove"/> Delete</p>
                                </li>
                            </ul>

                            {/* modal for note*/}
                            <div className="modal fade" id="noteFull" tabIndex="-1" role="dialog" aria-labelledby="myModalLabel">
                                <div className="modal-dialog" role="document">
                                    <div className="modal-content">
                                        <div className="modal-header">
                                            <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                                            <h4 className="modal-title" id="myModalLabel">Note</h4>
                                        </div>
                                        <div className="modal-body">
                                            <div dangerouslySetInnerHTML={{__html: data['content']}}></div>
                                            <hr/>
                                            Added at {data.date}
                                            <br/>
                                            <br/>
                                            Tags :
                                            {
                                                data['tag'].map(function (data, index) {
                                                    return (
                                                        <button className="btn btn-default" role="button" key={ index }>
                                                            #{data}
                                                        </button>
                                                    )
                                                })
                                            }
                                        </div>
                                        <div className="modal-footer">
                                            <button type="button" className="btn btn-default" data-dismiss="modal">
                                                <i className="fa fa-close"/> Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* modal component for note edit form*/}
                            <div className="modal fade" id="noteEdit" tabIndex="-1" role="dialog" aria-labelledby="myModalLabel">
                                <div className="modal-dialog" role="document">
                                    <div className="modal-content">
                                        <div className="modal-header">
                                            <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                                            <h4 className="modal-title" id="myModalLabel">Note</h4>
                                        </div>
                                        <div className="modal-body">
                                            <form className="form-horizontal" onSubmit={this.form.bind(this)}>
                                                <input type="hidden" value={data.id} ref="id"/>
                                                <input type="hidden" value={data.key} ref="key"/>
                                                <input type="hidden" value={data.iv} ref="iv"/>
                                                <div className="form-group">
                                                    <label className="control-label col-sm-2">Content</label>
                                                    <div className="col-sm-10">
                                                        <textarea id="editNote" defaultValue={data['content']}
                                                                  ref="content" className="form-control" placeholder="Enter Content"/>
                                                    </div>
                                                </div>
                                                <div className="form-group">
                                                    <div className="col-sm-offset-2 col-sm-10">
                                                        <button type="submit" className="btn btn-default"><i className="fa fa-save"/> Update
                                                        </button>
                                                    </div>
                                                </div>
                                            </form>
                                        </div>
                                        <div className="modal-footer">
                                            <button type="button" className="btn btn-default" data-dismiss="modal">
                                                <i className="fa fa-close"/> Cancel</button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            )
        });
    }

    render() {
        if (this.props.route.notes.loaded) {
            return (
                <div >
                    <Helmet
                        title="Hiren-Diary: Notes"
                        link={[
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic"},
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/card.css"}
            ]}
                    />
                    <div className="container">
                        <div className="row">
                            <div id="card">
                                {this.bunny()}
                            </div>
                        </div>
                    </div>
                </div>
            )
        }
        return (

            <div>
                <Helmet
                    title="Hiren-Diary: Notes"
                    link = {[
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic"},
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/card.css"}
            ]}
                />
                <h3>{this.props.route.notes.loadingText} </h3>
            </div>
        )
    }

}