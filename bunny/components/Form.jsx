import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';
import {Crypt} from '../utils/Crypt';


export default class Form extends React.Component {

    form(e) {
        /***
         * Handle ajax
         */
        e.preventDefault();
        let _url = this.postType() ? '/api/movies/' : '/api/notes/';
        let random = Math.random().toString(36).substr(2, 5);
        axios({
            method: 'post',
            url: _url,
            data: {
                'tag' : [ReactDOM.findDOMNode(this.refs.tag).value],
                'title': ReactDOM.findDOMNode(this.refs.title).value,
                'content': ReactDOM.findDOMNode(this.refs.content).value,
                'iv': random,
                'date': ReactDOM.findDOMNode(this.refs.date).value
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
        })
    }
    
    postType(e) {
        if(e.target.value == 'note') {
            $('#title').hide();
            return false;
        }
        else if (e.target.value == 'diary') {
            $('#title').show();
            return true;
        }
    }

    componentDidMount() {
        $('#summernote').summernote({  // initializer for summernote
            height: 150
        });


        $('#datetimepicker').datetimepicker({  // initializer for datetimepicker
            format: 'Y-mm-D H:mm:ss'
        });

        (function () { // function for selectize
            axios.get('/api/tags/', {
                headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
            }).then(function (response) {
                let nisha = [];
                response.data.map(function (hiren) {
                    let bunny = {'value': '', 'text': ''};
                    bunny['value'] = hiren.name;
                    bunny['text'] = hiren.name;
                    nisha.push(bunny);
                });
                $('#tags').selectize({
                    delimiter: ', ',
                    persist: false,
                    options: nisha,
                    create: function(input) {
                        return {
                            value: input,
                            text: input
                        }
                    }
                })
            }).catch(function (error) {
                console.error(error);
            })
        })();

        var cipher = forge.cipher.createCipher('AES-CBC', this.stringToBytes('s'));
         cipher.start({iv: "sasdrsdffcdfasdfercf34rc3c3c"});
         cipher.update(forge.util.createBuffer("Sasasasa"));
         cipher.finish();
         var encrypted = cipher.output;
         console.log(encrypted);
         console.log(encrypted.toHex());
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
                            <div className="form-group" >
                                <label className="control-label col-sm-3">Tags</label>
                                <div className="col-sm-9">
                                    <input type="text" ref="tag" id="tags" required className="form-control input-lg" />
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