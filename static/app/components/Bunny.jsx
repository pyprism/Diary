import React from 'react';
import Helmet from "react-helmet";

var $script = require("scriptjs");

$script("../../static/js/jquery-1.11.2.min.js", function() {
    $script('../../static/js/bootstrap.min.js', function () {
        $script('../../static/js/sidebar_menu.js', function () {
            $script('../../static/js/sweetalert.min.js');
        })
    });
});

export default class Bunny extends React.Component {
    render() {
        return (
            <div>
                <Helmet
                    title="Diary: Dashboard"
                    link={[
                    {"rel": "shortcut icon", "href": "/static/favicon.ico"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/bootstrap.min.css"},
                    {"rel": "stylesheet", "type":"text/css", "href": "/static/css/simple-sidebar.css"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/font-awesome.min.css"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/sweetalert.css"}
                ]}
                />

                <nav className="navbar navbar-default no-margin">
                    <div className="navbar-header fixed-brand">
                        <button type="button" className="navbar-toggle collapsed" data-toggle="collapse"  id="menu-toggle">
                            <span className="glyphicon glyphicon-th-large" aria-hidden="true" />
                        </button>
                        <a className="navbar-brand" href="#">
                            <i className="fa fa-heartbeat fa-4" /> Hiren-Diary</a>
                    </div>

                    <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                        <ul className="nav navbar-nav">
                            <li className="active" ><button className="navbar-toggle collapse in" data-toggle="collapse" id="menu-toggle-2"> <span className="glyphicon glyphicon-th-large" aria-hidden="true" /></button></li>
                        </ul>
                    </div>
                </nav>
            </div>
        )
    }
}