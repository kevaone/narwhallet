new (function wt() {
    self.addEventListener('message', function (e) { w(e.data); }, false);

    function c(response) { self.postMessage(response); };

    function w(e) {
        let x = new XMLHttpRequest();
        x.onreadystatechange = function () {
            let r = this.readyState;
            let s = this.status;
            if (r == 4 && s == 200) { console.log(this.responseText); c(JSON.parse(this.responseText)); }
            else if (r == 4 && s >= 400) { console.log(this.responseText); c(JSON.parse(this.responseText)); }
            else if (r == 4 && s >= 500) { console.log(this.responseText); c(JSON.parse(this.responseText)); }
        };
        x.open('POST', '$who/_kv/'+e['endPoint'], true);
        //x.setRequestHeader('Authorization', e['auth']);
        x.setRequestHeader('Access-Control-Allow-Origin', '*');
        //x.setRequestHeader('Content-type', 'application/json');
        x.setRequestHeader('Content-type', 'text/plain');
        x.send(JSON.stringify(e['data']));
    };
});