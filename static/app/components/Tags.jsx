import React from 'react';
import Sidebar from './Sidebar.jsx';
import Bunny from "./Bunny.jsx";


export default class Tags extends React.Component {
    render() {
        return (
            <div>
                <Bunny />
                 <div id="wrapper">
                     <Sidebar />
                <div id="page-content-wrapper">
                    <div className="container-fluid xyz">
                        <div className="row">
                            <div className="col-lg-12">
                                <h1>Tag <a href="http://seegatesite.com/create-simple-cool-sidebar-menu-with-bootstrap-3/" >Seegatesite.com</a></h1>
                                <p>This sidebar is adopted from start bootstrap simple sidebar startboostrap.com, which I modified slightly to be more cool. For tutorials and how to create it , you can read from my site here <a href="http://seegatesite.com/create-simple-cool-sidebar-menu-with-bootstrap-3/">create cool simple sidebar menu with boostrap 3</a></p>
                            </div>
                        </div>
                    </div>
                </div>
                     </div>
            </div>
        )
    }
}