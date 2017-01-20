/**
 * Created by prism on 1/11/17.
 */

import { browserHistory } from 'react-router';
import {Diary} from '../models/Diary.jsx';

export default class Crypt {
    static encrypt(text, key, iv) {
        var cipher = forge.cipher.createCipher('AES-CBC', key);
        cipher.start({iv: iv});
        cipher.update(forge.util.createBuffer(text));
        cipher.finish();
        var encrypted = cipher.output;
        return encrypted.toHex();
    }

    static decrypt(encryptedHex, key, iv) {
        var decipher = forge.cipher.createDecipher('AES-CBC', key);
        decipher.start({iv: forge.util.hexToBytes(iv)});
        decipher.update(forge.util.createBuffer(forge.util.hexToBytes(encryptedHex)));
        let bunny = decipher.finish();
        if(!bunny) {
            let dir = new Diary();
            dir.reset();
            browserHistory.push('/secret');
            sweetAlert("Error", "Secret key is not valid!", "error");
        }
        return decipher.output.data;
    }
}