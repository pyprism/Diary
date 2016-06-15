export default class Crypt {

    static encrypt(password, data) {
        var options = {
            data: data,
            passwords: [password]
        };
        openpgp.initWorker({ path:'../../static/bower/openpgp/dist/openpgp.worker.min.js' });
        openpgp.config.aead_protect = true;

        return openpgp.encrypt(options);
    }

    static decrypt(password, data) {
        var options = {
            message: openpgp.message.readArmored(data), // parse encrypted bytes
            password: [password]                 // decrypt with password
        };
        openpgp.initWorker({path: '../../static/bower/openpgp/dist/openpgp.worker.min.js'});
        openpgp.config.aead_protect = true;

        return openpgp.decrypt(options);
    }
}