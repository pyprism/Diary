import React from 'react';
import ReactDOM from 'react-dom';
import Helmet from "react-helmet";
import axios from 'axios';
import { browserHistory } from 'react-router';
import Crypt from '../utils/Crypt';


export default class Form extends React.Component {

    form(e) {
        /***
         * Handle post save
         */
        e.preventDefault();
        console.log(ReactDOM.findDOMNode(this.refs.tag).value);
        if(ReactDOM.findDOMNode(this.refs.postType).value == 'note')
            var _url = '/api/notes/';
        else if(ReactDOM.findDOMNode(this.refs.postType).value == 'diary')
            var _url = '/api/diary/';
        let  random = forge.random.getBytesSync(16),
            _salt = forge.random.getBytesSync(128),
            key = forge.pkcs5.pbkdf2(sessionStorage.getItem('key'), _salt, 100, 16);
        axios({
            method: 'post',
            url: _url,
            data: {
                'tag' : [ReactDOM.findDOMNode(this.refs.tag).value],
                'title': Crypt.encrypt(ReactDOM.findDOMNode(this.refs.title).value, key, random),
                'content': Crypt.encrypt(ReactDOM.findDOMNode(this.refs.content).value, key, random),
                'iv': forge.util.bytesToHex(random),
                'salt': forge.util.bytesToHex(_salt),
                'date': ReactDOM.findDOMNode(this.refs.date).value
            },
            headers: {
                'Authorization': "JWT " + sessionStorage.getItem('token')
            }
        }).then(function (response) {
            console.log(response);
            if(response.statusText === "Created") {
                sweetAlert("Saved", "Saved Successfully", "success");
                //browserHistory.push('/dashboard/');
            }
        }).catch(function (error) {
            if(error.statusText === 'Forbidden') {
                sweetAlert("Oops!", 'Token Expired, Log Out Plz !', "error");
            }
            console.error(error);
            sweetAlert('Error', error.statusText, 'error');
        })
    }

    postType(e) {
        if(e.target.value == 'note')
            $('#title').hide();
        else if (e.target.value == 'diary')
            $('#title').show();
    }

    componentDidMount() {
        $('#summernote').summernote({  // initializer for summernote
            height: 150
        });


        $('#datetimepicker').datetimepicker({  // initializer for datetimepicker
            format: 'YYYY-MM-D H:mm:ss'
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
                    delimiter: ' ',
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

                <form className="form-horizontal" onSubmit={this.form.bind(this)}>
                    <div className="form-group">
                        <label className="control-label col-sm-2">Post Type</label>
                        <div className="col-sm-10">
                            <select className="form-control " ref="postType" onChange={this.postType.bind(this)} required>
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