import React from 'react';
import {Link} from 'react-router';


export default class Sidebar extends React.Component {

    logout(){
        sessionStorage.removeItem('token');
    }

    render() {
        return (
            <div>

                <div id="sidebar-wrapper">
            <ul className="sidebar-nav nav-pills nav-stacked" id="menu">

                <li class="active">
                    <Link to="/dashboard/" activeStyle={{ color: '#315561'}}><span className="fa-stack fa-lg pull-left"><i className="fa fa-dashboard fa-stack-1x " /></span> Dashboard</Link>
                       <ul className="nav-pills nav-stacked bunny" >
                        <li><a href="simple_sidebar_menu.html#">link1</a></li>
                        <li><a href="simple_sidebar_menu.html#">link2</a></li>
                    </ul>
                </li>
                <li>
                    <a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i className="fa fa-flag fa-stack-1x "/></span> Shortcut</a>
                    <ul className="nav-pills nav-stacked bunny">
                        <li><a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i className="fa fa-flag fa-stack-1x "/></span>link1</a></li>
                        <li><a href="simple_sidebar_menu.html#"><span className="fa-stack fa-lg pull-left"><i className="fa fa-flag fa-stack-1x " /></span>link2</a></li>

                    </ul>
                </li>
                <li>
                     <Link to="/dashboard/tags" activeStyle={{ color: '#315561'}}> <span className="fa-stack fa-lg pull-left"><i className="fa fa-tags fa-stack-1x "/></span> Tags</Link>
                </li>
                <li>
                     <Link to="/" activeStyle={{ color: '#315561'}} onclick= { this.logout }> <span className="fa-stack fa-lg pull-left"><i className="fa fa-sign-out fa-stack-1x "/></span> Log Out</Link>
                </li>
            </ul>
        </div>

            </div>
        )
    }
}