import React from 'react';
import {Link} from 'react-router';


export default class Sidebar extends React.Component {
    render() {
        return (
            <div>
                <nav className="navbar navbar-default no-margin">
                    {/* Brand and toggle get grouped for better mobile display */}
                    <div className="navbar-header fixed-brand">
                        <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" id="menu-toggle">
                            <span className="glyphicon glyphicon-th-large" aria-hidden="true"></span>
                        </button>
                        <a className="navbar-brand" href="#"><i className="fa fa-rocket fa-4"></i>
                            Hiren</a>
                    </div>
                    {/* navbar-header */}

                    <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                        <ul className="nav navbar-nav">
                            <li className="active">
                                <button className="navbar-toggle collapse in" data-toggle="collapse" id="menu-toggle-2">
                                    <span className="glyphicon glyphicon-th-large" aria-hidden="true"></span></button>
                            </li>
                        </ul>
                    </div>
                    {/* bs-example-navbar-collapse-1 */}
                </nav>
                <div id="wrapper">
                    {/* Sidebar */}
                    <div id="sidebar-wrapper">
                        <ul className="sidebar-nav nav-pills nav-stacked" id="menu">

                            <li className="active">
                                <a href="#"><span className="fa-stack fa-lg pull-left"><i
                                    className="fa fa-dashboard fa-stack-1x "></i></span> Dashboard</a>
                                <ul className="nav-pills nav-stacked" style="list-style-type:none;">
                                    <li><a href="simple_sidebar_menu.html#">link1</a></li>
                                    <li><a href="simple_sidebar_menu.html#">link2</a></li>
                                </ul>
                            </li>
                            <li>
                                <a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i
                                    className="fa fa-flag fa-stack-1x "></i></span> Shortcut</a>
                                <ul className="nav-pills nav-stacked" style="list-style-type:none;">
                                    <li><a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i
                                        className="fa fa-flag fa-stack-1x "></i></span>link1</a></li>
                                    <li><a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i
                                        className="fa fa-flag fa-stack-1x "></i></span>link2</a></li>

                                </ul>
                            </li>
                            <li>
                                <a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i
                                    className="fa fa-cloud-download fa-stack-1x "></i></span>Overview</a>
                            </li>
                            <li>
                                <a href="simple_sidebar_menu.html#"> <span className="fa-stack fa-lg pull-left"><i
                                    className="fa fa-cart-plus fa-stack-1x "></i></span>Events</a>
                            </li>
                            <li>
                                <a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i
                                    className="fa fa-youtube-play fa-stack-1x "></i></span>About</a>
                            </li>
                            <li>
                                <a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i
                                    className="fa fa-wrench fa-stack-1x "></i></span>Services</a>
                            </li>
                            <li>
                                <a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i
                                    className="fa fa-server fa-stack-1x "></i></span>Contact</a>
                            </li>
                        </ul>
                    </div>
                </div>
                )
                }
                }