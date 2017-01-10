import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';


export default class Form extends React.Component {

    form(e) {
        /***
         * Handle ajax
         */
        e.preventDefault();
        console.log(ReactDOM.findDOMNode(this.refs.content).value);
        /* axios({
         method: 'post',
         url: '/api/movies/',
         data: {
         'movie' : {
         'name': ReactDOM.findDOMNode(this.refs.name).value,
         'imdb_rating': ReactDOM.findDOMNode(this.refs.imdb_rating).value,
         'movie_type': ReactDOM.findDOMNode(this.refs.movie_type).value
         },
         'rating': ReactDOM.findDOMNode(this.refs.rating).value,
         'source': ReactDOM.findDOMNode(this.refs.source).value,
         'video_quality': ReactDOM.findDOMNode(this.refs.video_quality).value,
         'watched_at': ReactDOM.findDOMNode(this.refs.watched_at).value,
         'watched_full': ReactDOM.findDOMNode(this.refs.watched_full).value
         },
         headers: {
         'Authorization': "JWT " + sessionStorage.getItem('token')
         }
         }).then(function (response) {
         if(response.statusText === "Created") {
         sweetAlert("Saved", "New Movie Saved Successfully", "info");
         browserHistory.push('/dashboard/');
         }
         }).catch(function (error) {
         console.error(error);
         sweetAlert('Error', 'Check console!', 'error');
         })*/
    }

    postType(e) {
        if(e.target.value == 'note')
            $('#title').hide();
        else if (e.target.value == 'diary')
            $('#title').show();
    }

    componentDidMount() {
        $('#summernote').summernote({
            height: 150
        });


        $('#datetimepicker').datetimepicker({
            format: 'Y-mm-D H:mm:ss'
        });


    }

    render() {

        return (
            <div className="container">
                <div className="row">
                    <Helmet
                        title="Hiren-Diary: Form"
                    />
                    <div className="col-sm-6 col-sm-offset-2">
                        <form className="form-horizontal pad-bg" onSubmit={this.form.bind(this)}>
                            <h4 className="text-center">Create New Post</h4>
                            <div className="form-group">
                                <label className="control-label col-sm-3">Post Type</label>
                                <div className="col-sm-9">
                                    <select className="form-control input-lg" onChange={this.postType.bind(this)} required>
                                        <option value="diary">Diary</option>
                                        <option value="note">Note</option>
                                    </select>
                                </div>
                            </div>
                            <div className="form-group" id="title">
                                <label className="control-label col-sm-3">Title</label>
                                <div className="col-sm-9">
                                    <input type="text" ref="title" required placeholder="Title of the post" className="form-control input-lg" />
                                </div>
                            </div>
                            <div className="form-group" id="title">
                                <label className="control-label col-sm-3">Content</label>
                                <div className="col-sm-9">
                                    <textarea id="summernote" type="text" ref="content" required placeholder="Title of the post" className="form-control input-lg" />
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="control-label col-sm-3">Date</label>
                                <div className='input-group date' id='datetimepicker'>
                                    <input type='text' ref="date" className="form-control input-lg" />
                                    <span className="input-group-addon">
                                        <span className="glyphicon glyphicon-calendar" />
                                    </span>
                                </div>
                            </div>
                            <div className="form-group" id="title">
                                <label className="control-label col-sm-3">Tags</label>
                                <div className="col-sm-9">
                                    <input type="text" ref="tag" required className="form-control input-lg" />
                                </div>
                            </div>
                            <div className="form-group">
                                <div className="col-sm-offset-3 col-sm-9">
                                    <button type="submit" className="btn btn-default btn-lg"><i className="fa fa-save"></i> Save</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        )
    }

}