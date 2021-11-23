var nww_main = new (function () {
    let Q = new Worker('/js/worker.js');

    function nww_main() {
        //console.log("main");
    };

    nww_main.prototype.action = function (action_type, tx) {
        let _pl = {};
        _pl['endPoint'] = action_type;
        _pl['data'] = {'date': Date.now(), 'data': 'datter', 'tx': tx};
        Q.postMessage(_pl);
    };

    Q.onmessage = function(e) {
        console.log('Message received from worker', e['data']);
    };

    return new nww_main();

});