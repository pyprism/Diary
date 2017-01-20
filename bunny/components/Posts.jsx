import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { toJS } from "mobx";
import { browserHistory } from 'react-router';
import { observer } from "mobx-react";
import {Link} from 'react-router';


@observer
export default class Posts extends React.Component {

    componentDidMount(){
        this.props.route.posts.getPosts();
    }

    hiren() {
        var bunny = [];
        (this.props.route.posts.posts).map(function (data) {
            bunny.push(
                <div className="post-preview" key={ data.id }>
                    <Link to={'/dashboard/posts/' + data.id + '/'}>
                        <h2 className="post-title">
                            {data.title}
                        </h2>
                    </Link>
                    <p className="post-meta">Posted on {data.date}</p>
                </div>
            )
        });
        return (
            <div> {bunny} </div>
        );
    }

    render() {

        if(this.props.route.posts.loaded){
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

                                {this.hiren()}
                            </div>
                        </div>
                    </div>

                </div>
            )
        }
        return (

            <div>
                <Helmet
                    title="Hiren-Diary: Posts"
                    link = {[
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic"},
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/hiren.css"}
            ]}
                />
                <h3>{this.props.route.posts.loadingText} </h3>
            </div>
        )

    }
}