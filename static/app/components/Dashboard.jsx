import React from 'react';
import ReactDOM from 'react-dom';
import { observable, computed } from "mobx";
import { observer } from "mobx-react";
import Sidebar from "./Sidebar.jsx";
import Page from "./Page.jsx";
import Bunny from "./Bunny.jsx";


@observer export default class Dashboard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            x: "hello"
        };
    }

    render() {
        return (
            <div>
                <Bunny />
                <div id="wrapper">
                    <Sidebar />
                    <Page />
                </div>
            </div>
        )
    }
}