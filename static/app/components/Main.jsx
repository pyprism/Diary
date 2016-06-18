import React from 'react';
import Helmet from "react-helmet";
import {Link} from 'react-router';
import { browserHistory } from 'react-router';


export default class Main extends React.Component {

    logout(){
        sessionStorage.clear();
        browserHistory.push('/');
    }

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
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/bower/sweetalert/dist/sweetalert.css"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/bower/jqcloud2/dist/jqcloud.css"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/bower/summernote/dist/summernote.css"},
                    {"rel": "stylesheet", "type": "text/css", "href": "/static/css/bootstrap-datepicker3.standalone.min.css"}
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

                <div id="wrapper">
                    <div id="sidebar-wrapper">
                        <ul className="sidebar-nav nav-pills nav-stacked" id="menu">

                            <li class="active">
                                <Link to="/dashboard/stats/" activeStyle={{ color: '#315561'}}><span className="fa-stack fa-lg pull-left"><i className="fa fa-dashboard fa-stack-1x " /></span> Dashboard</Link>
                            </li>
                            <li>
                                <Link to="/dashboard/posts/"><span className="fa-stack fa-lg pull-left"><i className="fa fa-archive fa-stack-1x "/></span> Posts</Link>
                                <ul className="nav-pills nav-stacked bunny">
                                    <li><Link to="/dashboard/create/"><span className="fa-stack fa-lg pull-left"><i className="fa fa-file-text fa-stack-1x "/></span> Create New Post</Link></li>
                                </ul>
                            </li>
                            <li>
                                <Link to="/dashboard/tags" activeStyle={{ color: '#315561'}}> <span className="fa-stack fa-lg pull-left"><i className="fa fa-tags fa-stack-1x "/></span> Tags</Link>
                            </li>
                            <li>
                                <Link  to="#" activeStyle={{ color: '#315561'}} onClick= { this.logout }> <span className="fa-stack fa-lg pull-left"><i className="fa fa-sign-out fa-stack-1x "/></span> Log Out</Link>
                            </li>
                        </ul>
                    </div>
                    <div id="page-content-wrapper">
                        <div className="container-fluid xyz">
                            <div className="row">
                                <div className="col-lg-12">
                                    {this.props.children}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}