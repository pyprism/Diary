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

    componentDidMount() {
        this.props.route.posts.pageId = this.props.params.id;
        this.props.route.posts.findPostById();
        console.log(toJS(this.props.route.posts.post['tag']));
    }

    delete() {
        axios({
            method: 'delete',
            url: '/api/diary/' + this.props.route.posts.pageId + '/',
            headers: {
                'Authorization': "JWT " + sessionStorage.getItem('token')
            }
        })
    }

    tags() {
        var bunny = [];
        (this.props.route.posts.post['tag']).map(function (data) {
            bunny.push(
                <button className="btn btn-default" role="button" >
                    #{data}
                </button>
            )
        });
        return (
            <div> {bunny} <Link className="btn btn-info"
                                 to={'/dashboard/posts/' + this.props.route.posts.pageId + '/edit/'}
                                 role="button">Edit</Link>
                <button className="btn btn-danger"  role="button" onClick={this.delete()}>Delete</button>
            </div>
        );
    }

    render() {
        return (
            <div className="posts">
                <Helmet
                    title="Hiren-Diary: Post"
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