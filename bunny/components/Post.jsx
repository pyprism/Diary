import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { toJS } from "mobx";
import { browserHistory } from 'react-router';
import { observer } from "mobx-react";
import {Link} from 'react-router';


@observer
export default class Post extends React.Component {
    /**
     * Handle the post, tag and edit and delete button
     */

    componentDidMount() {
        this.props.route.posts.pageId = this.props.params.id;
        this.props.route.posts.findPostById();
    }

    deletePost() {  // delete button
        var id = this.props.route.posts.pageId;

        let message = "Delete the post",
            title = "Are you sure ?";
        eModal.confirm(message, title)
            .then(function(){
                axios({
                    method: 'delete',
                    url: '/api/diary/' + id + '/',
                    headers: {
                        'Authorization': "JWT " + sessionStorage.getItem('token')
                    }
                }).then(function (data) {
                    sweetAlert("Deleted", "Post deleted", "success");
                    browserHistory.push('/dashboard/posts/');
                }).catch(function (error) {
                    sweetAlert("Error", "Error in deletion!", "error");
                })
            }, function(){

            });
    }

    tags() { // generate tags
        var bunny = [];
        if(this.props.route.posts.post['tag']) {
            (this.props.route.posts.post['tag']).map(function (data, index) {
                bunny.push(
                    <button className="btn btn-default" role="button" key={ index }>
                        #{data}
                    </button>
                )
            });
            return (
                <div> Tags: {bunny}
                    <hr/>
                    <Link className="btn btn-info"
                          to={'/dashboard/posts/' + this.props.route.posts.pageId + '/edit/'}
                          role="button">Edit</Link>

                    <button className="btn btn-danger"  onClick={this.deletePost.bind(this)}>Delete</button>
                </div>
            );
        }
    }

    render() {
        var _title = 'Hiren-Diary: ' + this.props.route.posts.post['title'];

        return (
            <div className="posts">
                <Helmet
                    title= {_title}
                    link = {[
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic"},
                    {"rel": "stylesheet", "type": "text/css", "href": "https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/hiren.css"}
            ]}
                />

                <div className="container">
                    <div className="row">
                        <h2 className="post-title">
                            {this.props.route.posts.post['title']}
                        </h2>
                        <hr/>
                        <article>
                            <div dangerouslySetInnerHTML={{__html: this.props.route.posts.post['content']}} />
                        </article>
                        <hr/>
                        <p className="post-meta">Posted on {this.props.route.posts.post['date']}</p>
                        {this.tags()}
                    </div>
                </div>

            </div>
        )
    }

}