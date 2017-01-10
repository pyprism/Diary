import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';


export default class Posts extends React.Component {
    render() {
        return (
            <div>
                <Helmet
                    title="Hiren-Diary: Posts"
                />
                I am fucking Posts
            </div>
        )
    }
}