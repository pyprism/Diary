import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';
import Crypt from '../utils/Crypt';


export default class Form extends React.Component {

    form(e) {
        /***
         * Handle ajax
         */
        e.preventDefault();
        let _url = this.postType() ? '/api/movies/' : '/api/notes/';
        let random = Math.random().toString(36).substr(2, 5);
        axios({
            method: 'post',
            url: _url,
            data: {
                'tag' : [ReactDOM.findDOMNode(this.refs.tag).value],
                'title': ReactDOM.findDOMNode(this.refs.title).value,
                'content': ReactDOM.findDOMNode(this.refs.content).value,
                'iv': random,
                'date': ReactDOM.findDOMNode(this.refs.date).value
            },
            headers: {
                'Authorization': "JWT " + sessionStorage.getItem('token')
            }
        }).then(function (response) {
            if(response.statusText === "Created") {
                sweetAlert("Saved", "New Movie Saved Successfully", "info");
                browserHistory.push('/dashboard/');
            }
        }).catch(function (error) {
            console.error(error);
            sweetAlert('Error', 'Check console!', 'error');
        })
    }

    postType(e) {
        if(e.target.value == 'note') {
            $('#title').hide();
            return false;
        }
        else if (e.target.value == 'diary') {
            $('#title').show();
            return true;
        }
    }

    str2ab(str) {
        var buf = new ArrayBuffer(str.length*2); // 2 bytes for each char
        var bufView = new Uint16Array(buf);
        for (var i=0, strLen=str.length; i<strLen; i++) {
            bufView[i] = str.charCodeAt(i);
        }
        return buf;
    }

    componentDidMount() {
        $('#summernote').summernote({  // initializer for summernote
            height: 150
        });


        $('#datetimepicker').datetimepicker({  // initializer for datetimepicker
            format: 'Y-mm-D H:mm:ss'
        });

        (function () { // function for selectize
            axios.get('/api/tags/', {
                headers: {'Authorization': "JWT " + sessionStorage.getItem('token')}
            }).then(function (response) {
                let nisha = [];
                response.data.map(function (hiren) {
                    let bunny = {'value': '', 'text': ''};
                    bunny['value'] = hiren.name;
                    bunny['text'] = hiren.name;
                    nisha.push(bunny);
                });
                $('#tags').selectize({
                    delimiter: ', ',
                    persist: false,
                    options: nisha,
                    create: function(input) {
                        return {
                            value: input,
                            text: input
                        }
                    }
                })
            }).catch(function (error) {
                console.error(error);
            })
        })();

        /*var salt = forge.random.getBytesSync(128);
         console.info(forge.util.bytesToHex(salt));
         var _iv = forge.random.getBytesSync(16);
         var key = forge.pkcs5.pbkdf2('password', salt, 64000, 16);
         var cipher = forge.cipher.createCipher('AES-CBC', key);
         cipher.start({iv: _iv});
         cipher.update(forge.util.createBuffer("Sasasasa"));
         cipher.finish();
         var encrypted = cipher.output;
         //console.log(encrypted);
         //console.log(encrypted.toHex());
         //console.log(forge.util.hexToBytes(encrypted.toHex()));

         var decipher = forge.cipher.createDecipher('AES-CBC', key);
         decipher.start({iv: _iv});
         decipher.update(encrypted);
         decipher.finish();
         // outputs decrypted hex
         //console.log(decipher.output.data);*/
    }

    render() {

        return (
            <div >
                <div className="row">
                    <Helmet
                        title="Hiren-Diary: Form"
                    />
                </div>

                <form className="form-horizontal">
                    <div className="form-group">
                        <label className="control-label col-sm-2">Post Type</label>
                        <div className="col-sm-10">
                            <select className="form-control " onChange={this.postType.bind(this)} required>
                                <option value="diary">Diary</option>
                                <option value="note">Note</option>
                            </select>
                        </div>
                    </div>
                    <div className="form-group" id="title">
                        <label className="control-label col-sm-2" >Title</label>
                        <div className="col-sm-10">
                            <input type="text" className="form-control" ref="title" placeholder="Post Title"/>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="control-label col-sm-2" >Content</label>
                        <div className="col-sm-10">
                            <textarea id="summernote" ref="content" className="form-control" placeholder="Enter Content"/>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="control-label col-sm-2">Date</label>
                        <div className='input-group date' id='datetimepicker'>
                            <input type='text' ref="date" className="form-control" />
                                    <span className="input-group-addon">
                                        <span className="glyphicon glyphicon-calendar" />
                                    </span>
                        </div>
                    </div>
                    <div className="form-group" >
                        <label className="control-label col-sm-2">Tags</label>
                        <div className="col-sm-10">
                            <input type="text" ref="tag" id="tags" required className="form-control input-lg" />
                        </div>
                    </div>
                    <div className="form-group">
                        <div className="col-sm-offset-2 col-sm-10">
                            <button type="submit" className="btn btn-default"><i className="fa fa-save" /> Save</button>
                        </div>
                    </div>
                </form>
            </div>
        )
    }

}