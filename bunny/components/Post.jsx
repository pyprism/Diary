import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { toJS } from "mobx";
import { browserHistory } from 'react-router';
import { observer } from "mobx-react";


@observer
export default class Post extends React.Component {
    
    componentDidMount() {
        this.props.route.posts.pageId = this.props.params.id;
        this.props.route.posts.findPostById();
    }
    
    render() {
        return (
            <div>
                <Helmet
                        title="Hiren-Diary: Post"
                        link = {[
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic"},
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/hiren.css"}
            ]}
                    />
                <article>
                    <h1>{this.props.route.posts.post['title']}</h1>
                </article>
            </div>
        )
    }

}