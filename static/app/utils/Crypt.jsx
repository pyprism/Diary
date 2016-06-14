export default class Crypt {
   // constructor() {
   //     this.openpgp = window.openpgp;
   //     this.openpgp.initWorker({ path:'../../static/bower/openpgp/dist/openpgp.worker.min.js' });
   //     this.openpgp.config.aead_protect = true;
   // }

    static *encrypt(password, data) {
        var options, encrypted;
        options = {
            data: data,
            passwords: [password]
        };
        let openpgp = window.openpgp;
        openpgp.initWorker({ path:'../../static/bower/openpgp/dist/openpgp.worker.min.js' });
        openpgp.config.aead_protect = true;
       /* openpgp.encrypt(options).then(function(ciphertext) {
            //return encrypted = ciphertext.data;
            console.log(ciphertext.data);
            //return ciphertext.data;
        });*/
        let bunny = yield openpgp.encrypt(options);
        return bunny.data;
    }

    /*decrypt(password, data) {
        options = {
            message: this.openpgp.message.readArmored(data), // parse encrypted bytes
            password: password                 // decrypt with password
        };

        this.openpgp.decrypt(options).then(function(plaintext) {
            return plaintext.data;
        });
    }*/
}