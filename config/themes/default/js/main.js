var nww_main = new (function () {
    let Q = new Worker('/js/worker.js');
    let modal = document.getElementById('modal-main');
    let modal_body = document.getElementById('modal-body');
    let modal_close = document.getElementById('modal-close');
    let modal_cancel = document.getElementById('modal-cancel');
    let modal_submit = document.getElementById('modal-submit');

    function nww_main() {
        //console.log('main');
        check_for_auction();

        modal_close.onclick = function() {
            modal.style.display = 'none';
            clear_modal();
        };

        modal_cancel.onclick = function() {
            modal.style.display = 'none';
            clear_modal();
        };

        modal_submit.onclick = function() {
            nww_main.prototype.action();
            modal.style.display = 'none';
            clear_modal();
        };

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = 'none';
                clear_modal();
            };
        };

        Q.onmessage = function(e) {
            console.log('Message received from worker', e['data']);
        };
    };

    nww_main.prototype.action_modal = function (action_type, tx) {
        build_modal(action_type, tx);
        modal.style.display = 'block';
    };

    nww_main.prototype.action = function () {
        let _data = document.getElementById('modal-action-data');
        let _ref = document.getElementById('modal-action-ref').value.split(':');

        let _pl = {};
        _pl['endPoint'] = _ref[0];
        _pl['data'] = {'date': Date.now(), 'data': _data.value, 'tx': _ref[1]};
        Q.postMessage(_pl);
    };

    ce = function (e) {
        let r_e = document.createElement(e);
        return r_e;
    };

    function check_for_auction() {
        let _keys = document.querySelectorAll('[id^="rs-title-"]');
        if (_keys.length > 0) {
            if (_keys[0].innerHTML === 'NFT Auction') {
                let _data = document.getElementById('rs-actions');
                let d1 = ce('div');
                let i1 = ce('i');
                let _id = _keys[0].id.split('-')[2]
                d1.classList.add('vd');
                i1.classList.add('fas');
                i1.classList.add('fa-comment-dollar');
                d1.appendChild(i1);
                _data.appendChild(d1);
                d1.setAttribute('onclick', 'nww_main.action_modal(\'bid\', \''+_id+'\');');
            };
        };
    };

    function _clear_modal(section) {
        while (section.hasChildNodes()) {  
            section.removeChild(section.firstChild);
        };
    };

    function clear_modal() {
        let modal_header_content = document.getElementById('modal-header-content');
        _clear_modal(modal_header_content);
        _clear_modal(modal_body);
    };

    function build_modal(action_type, tx) {
        let modal_header_text = document.getElementById('modal-header-content');
        let title_key = document.getElementById('rs-title-'+tx)
        let d1 = ce('div');
        let d2 = ce('div');
        let d3 = ce('div');
        let d4 = ce('div');
        let h = ce('h2')
        let hi = ce('i')
        hi.classList.add('fas')
        let s1 = ce('h3');
        let s2 = ce('span');
        let inp1 = undefined
        let inp2 = ce('input');
        inp2.type = 'hidden';
        inp2.value = action_type+':'+tx;

        s1.innerText = title_key.innerText;

        if (action_type === 'reward') {
            inp1 = ce('input');
            inp1.type = 'text';
            h.innerText = 'Reward';
            hi.classList.add('fa-heart')
            s2.innerText = 'Reward Amount:';
            inp1.placeholder = '0';
        }
        else if (action_type === 'comment') {
            inp1 = ce('textarea');
            inp1.rows = 8
            inp1.cols = 35
            h.innerText = 'Comment';
            hi.classList.add('fa-comment-dots')
            s2.innerText = 'Comment:';
            inp1.placeholder = 'Comment';
        }
        else if (action_type === 'repost') {
            inp1 = ce('textarea');
            inp1.rows = 8
            inp1.cols = 35
            h.innerText = 'Repost';
            hi.classList.add('fa-retweet')
            s2.innerText = 'Repost:';
            inp1.placeholder = 'Repost';
        }
        else if (action_type === 'share') {
            inp1 = ce('textarea');
            h.innerText = 'Share';
            hi.classList.add('fa-external-link-alt')
            s2.innerText = 'Share:';
        }
        else if (action_type === 'bid') {
            inp1 = ce('input');
            inp1.type = 'text';
            inp1.placeholder = '0';
            h.innerText = 'Bid';
            hi.classList.add('fa-comment-dollar')
            s2.innerText = 'Bid Amount:';
        };

        inp1.id = 'modal-action-data';
        inp2.id = 'modal-action-ref';

        d1.appendChild(s1);
        d4.appendChild(hi);
        d4.appendChild(h);
        modal_header_text.appendChild(d4);
        modal_header_text.appendChild(d1);
        d2.appendChild(s2);
        d3.appendChild(inp1);
        d3.appendChild(inp2);

        modal_body.appendChild(d2);
        modal_body.appendChild(d3);
    };

    return new nww_main();

});