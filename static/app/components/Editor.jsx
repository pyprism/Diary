import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import Helmet from "react-helmet";
import { browserHistory } from 'react-router';
import Crypt from '../utils/Crypt.jsx';


export default class Editor extends React.Component {

    editor(e){
        e.preventDefault();
        console.log('pressed');
        Crypt.encrypt(sessionStorage.getItem('key'), 'x')
    }

    componentDidMount() {

        $(ReactDOM.findDOMNode(this)).ready(function () {
            $('#datetime').datepicker({
                autoclose: true,
                format: 'dd/mm/yyyy',
                clearBtn: true,
                todayBtn: true,
                todayHighlight: true,
                weekStart: 6
            });
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
                        <textarea name="text" required  ref="post" />
                    </div>
                    <div className="form-group">
                        <div className='input-group date' id='datetime' >
                    <div className="input-group-addon">
                        <span className="glyphicon glyphicon-calendar" />
                    </div>
                            <input type='text' className="form-control" ref="date" required  placeholder="Date"/>
                        </div>
                    </div>
                    <div className="form-group">
                        <input type="text" className="form-control" ref="tag" id="tag" placeholder="Tag"/>
                    </div>
                    <div className="form-group">
                        <button type="submit" className="btn btn-primary btn-lg btn-block">Save</button>
                    </div>
                </form>
            </div>
        )}}
