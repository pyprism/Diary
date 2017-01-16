import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';


export default class Posts extends React.Component {
    render() {
        return (
            <div className="posts">
                <Helmet
                    title="Hiren-Diary: Posts"
                    link = {[
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic"},
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/hiren.css"}
            ]}
                />
                <div className="container">
                    <div className="row">
                        <div className="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                            <div className="post-preview">
                                <a href="post.html">
                                    <h2 className="post-title">
                                        Man must explore, and this is exploration at its greatest
                                    </h2>
                                </a>
                                <p className="post-meta">Posted on September 24, 2014</p>
                            </div>
                            <div className="post-preview">
                                <a href="post.html">
                                    <h2 className="post-title">
                                        Man must explore, and this is exploration at its greatest
                                    </h2>
                                </a>
                                <p className="post-meta">Posted on September 24, 2014</p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        )
    }
}