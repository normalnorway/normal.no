//console.log (window.django);
//console.log (window.django.jQuery);


function $get (id) {
    return document.getElementById (id);
}


function ajax_upload (form, on_load, on_error)
{
    var xhr = new XMLHttpRequest();
    //xhr.onload = on_load || null;
    //xhr.onerror = on_error || function () { ... };
    if (on_load)
	xhr.onload = on_load;
    if (on_error)
	xhr.onerror = on_error;
    else
	xhr.onerror = function (ev) { error('ajax_upload', arguments, ev); }

    xhr.open ('POST', form.getAttribute('action'));
    xhr.setRequestHeader ('X-REQUESTED-WITH', 'XMLHttpRequest');
    xhr.send (new FormData(form));
}


// rename callback on_success or on_load? success_cb, error_cb
function get_json (url, callback)  // @todo on_error
{
    // XXX does error() exists?
    var xhr = new XMLHttpRequest();
    xhr.onerror = function (ev) { error('get_json', arguments, ev); };
    xhr.onload = function (ev) {
        // status always 2xxx when onerror handler defined?
        //console.assert (xhr.status != 200);
        callback (xhr.response);
    };
    xhr.open ('GET', url, true);
    xhr.responseType = 'json';
    xhr.setRequestHeader ('X-REQUESTED-WITH', 'XMLHttpRequest');
    xhr.send ();
}
