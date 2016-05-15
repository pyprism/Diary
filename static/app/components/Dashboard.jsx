import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
//import Sidebar from "./Sidebar.jsx";


export default class Dashboard extends React.Component {
    render() {
        return (
            <div>
                <Helmet
                    title="Diary: Dashboard"
                    link={[
                    {"rel": "stylesheet", "type": "text/css", "href": "static/css/bootstrap.min.css"},
                    {"rel": "stylesheet", "type":"text/css", "href": "static/css/simple-sidebar.css"},
                    {"rel": "stylesheet", "type": "text/css", "href": "static/css/font-awesome.min.css"}
                ]}
                   // script={[
                 // {"src": "static/js/jquery-1.11.2.min.js", "type": "text/javascript"},
                 // {"src": "static/js/bootstrap.min.js", "type": "text/javascript"},
                //  {"src": "static/js/sidebar_menu.js", "type": "text/javascript"},

               // ]}
                />
                
                <nav className="navbar navbar-default no-margin">
                <div className="navbar-header fixed-brand">
                    <button type="button" className="navbar-toggle collapsed" data-toggle="collapse"  id="menu-toggle">
                      <span className="glyphicon glyphicon-th-large" aria-hidden="true" />
                    </button>
                    <a className="navbar-brand" href="#"><i className="fa fa-rocket fa-4" /> Hiren</a>
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