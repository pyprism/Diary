import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';
import { observer } from "mobx-react";
import {Link} from 'react-router';


@observer
export default class Notes extends React.Component {

    componentDidMount() {
        this.props.route.notes.getNotes();
    }

    fullNote(){

    }

    editor(){
        this.props.route.notes.loaded = false;
    }

    deleteNote(id){
        $('[data-toggle=confirmation]').confirmation({
            rootSelector: '[data-toggle=confirmation]',
            onConfirm: function () {
                axios({
                    method: 'delete',
                    url: '/api/notes/' + id + '/',
                    headers: {
                        'Authorization': "JWT " + sessionStorage.getItem('token')
                    }
                }).then(function (data) {
                    sweetAlert("Deleted", "Note deleted", "success");
                    browserHistory.push('/dashboard/notes/');
                }).catch(function (error) {
                    sweetAlert("Warning", "Error in deletion", "error");
                })
            }
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
                                    <p className="text-a"><i className="fa fa-exclamation-circle"/> Read Full</p>
                                </li>
                                <li className="views">
                                    <p>
                                    <Link to={'/dashboard/notes/' + data.id + '/'} className="text-a">
                                        <i className="fa fa-edit"/> Edit</Link> </p>
                                </li>
                                <li className="comment">
                                    <p className="text-a" onClick={this.deleteNote(data.id)} data-toggle="confirmation" data-placement="bottom" > <i className="fa fa-remove"/> Delete</p>
                                </li>
                            </ul>
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