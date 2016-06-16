import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import Helmet from "react-helmet";
import { browserHistory } from 'react-router';

//var $ = require('../../js/jquery-1.11.2.min');
export default class Editor extends React.Component {

    editor(e){
        e.preventDefault();
        console.log('pressed');
    }

    componentDidMount() {

        $(ReactDOM.findDOMNode(this)).ready(function () {
            $('#datetimepicker1').datetimepicker();
            $('textarea').summernote({
            height: 300
        });
        })
    }

    render () {
        return (
            <div>
                <Helmet
                    title="Diary: Editor"
                />
                <form className="form col-md-12 center-block" onSubmit={this.editor.bind(this)} >
                    <div className="form-group">
                        <label >Title:</label>
                        <input type="text" required ref="title" className="form-control" name="title" />
                    </div>
                    <div className="form-group">
                        <label >Content:</label>
                        <textarea name="text" required ref="post" />
                    </div>
                    <div class="form-group">
                        <div className='input-group date' id='datetimepicker1'>
                            <input type='text' class="form-control" />
                    <span class="input-group-addon">
                        <span className="glyphicon glyphicon-calendar" />
                    </span>
                        </div>
                    </div>
                    <div className="form-group">
                        <button type="submit" className="btn btn-primary btn-lg btn-block">Save</button>
                    </div>
                </form>
            </div>
        )}}
