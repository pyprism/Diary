import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { toJS } from "mobx";
import { browserHistory } from 'react-router';
import { observer } from "mobx-react";


export default class Post extends React.Component {
    
    componentDidMount() {
        console.log(this.props.route.posts.findPostById(this.props.params.id));
    }
    
    render() {
        return (
            <div>
                Single Post
                {this.props.params.id}
            </div>
        )
    }

}