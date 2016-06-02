export default class Crypt {
    constructor() {
        this.openpgp = window.openpgp;
        this.openpgp.initWorker({ path:'../../static/openpgp/dist/openpgp.worker.min.js' });
        this.openpgp.config.aead_protect = true;
    }

    encrypt(password, data) {
        var options, encrypted;
        options = {
            data: data,
            passwords: [password]
        };

        this.openpgp.encrypt(options).then(function(ciphertext) {
            return encrypted = ciphertext.data;
        });
    }

    decrypt(password, data) {
        options = {
            message: this.openpgp.message.readArmored(data), // parse encrypted bytes
            password: password                 // decrypt with password
        };

        this.openpgp.decrypt(options).then(function(plaintext) {
            return plaintext.data;
        });
    }
}