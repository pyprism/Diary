import React from 'react';
import ReactDOM from 'react-dom';
import { observable, computed } from "mobx";
import { observer } from "mobx-react";
import Sidebar from "./Sidebar.jsx";
import Bunny from "./Bunny.jsx";
import GetSecretKey from "./GetSecretKey.jsx";
import SetSecretKey from "./SetSecretKey.jsx";


@observer export default class Dashboard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            x: "hello"
        };
    }

    bunny() {
        var secretkey;
        try {
            if(sessionStorage.getItem('key')) {
                return secretkey = < GetSecretKey key={sessionStorage.getItem('key')} />;
            } else {
               return  secretkey = < SetSecretKey />;
            }
        } catch (e) {
            if (e instanceof ReferenceError) {
                return secretkey = < SetSecretKey />;
            }
        }
    }

    render() {

        var secretkey;
            if(sessionStorage.getItem('key')) {
                secretkey = < GetSecretKey key={sessionStorage.getItem('key')} />;
            } else {
               secretkey = < SetSecretKey />;
            }


        return (
            <div>
                <Bunny />
                <div id="wrapper">
                    <Sidebar />
                    <div id="page-content-wrapper">
                        <div className="container-fluid xyz">
                            <div className="row">
                                <div className="col-lg-12">
                                    { secretkey }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}