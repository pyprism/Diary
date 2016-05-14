import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";

export default class Dashboard extends React.Component {
    render() {
        return (
            <div>
                <Helmet
                    title="Diary: Dashboard"
                    link={[
                    {"rel": "stylesheet", "href": "/css/bootstrap.min.css"},
                    {"rel": "stylesheet", "href": "/css/simple-sidebar.css"},
                    {"rel": "stylesheet", "href": "/css/font-awesome.min.css"}
                ]}
                />
            </div>
        )
    }
}