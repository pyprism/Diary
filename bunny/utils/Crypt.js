/**
 * Created by prism on 1/11/17.
 */

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
        decipher.start({iv: iv});
        decipher.update(forge.util.hexToBytes(encryptedHex));
        decipher.finish();
        return decipher.output.data;
    }
}