/**
 * DjangoMCE - Django TinyMCE4 plugin.
 *
 * TinyMCE namespace: window.tinymce
 *
 * Our namespace: window.djangomce
 *
 * TODO:
 * - csrf protection for tinymce_upload
 *   var csrf = $cookie ('csrftoken');
 * - don't depend on core.js
 */


// Django TinyMCE4 namespace
window.djangomce =
{
    config: {},
    cache: {},

//    upload: function (form, output) { ... },
};



// @todo only install if needed
document.addEventListener ("DOMContentLoaded", function (ev)
{
    ev.target.body.innerHTML +=
        '<form id="tinymce-upload-form" action="/tinymce/upload/" method="post" enctype="multipart/form-data" style="display:none">' +
        '  <input type="file" id="tinymce-file-input" name="must-have-a-name" />' +
        '</form>';
});



function tinymce_upload (form, output)
{
    ajax_upload (form, function (ev) {
	var response = ev.target.responseText;
	var A = response.split (' ', 2);
	console.assert (A[0]=='OK', 'upload error:', response.substring(0,4096));
	output.value = A[1];
    });
}



/*
function get_json (url, callback)
{
    tinymce.util.XHR.send ({url: url, success: function (text) {
        callback (tinymce.util.JSON.parse(text));
    }});
}
*/



/** TinyMCE4 config.
 *
 * TODO:
 * - font sizes / small style
 * - semantic clases (from style.less)
 * - need way to override default config per widget?
 */

tinymce.init ({
    selector: 'textarea.tinymce',

    width: 730,
    height: 550,
    resize: 'both',

    // @todo test
    // statusbar : false,
    // indentation
    // valid_classes
    // body_id	    // use this id for TinyMCE specific overrides in content_css
    //toolbar: "insertfile
    //preview_styles

    // Extra drop-down in add link popup to add class to link.
    /*
    link_class_list: [
        {title: 'None', value: ''},
        {title: 'Internal', value: ''}
        {title: 'External', value: 'external-link'},
    ],
    */

    content_css: '/static/css/tinymce.css',
    //content_css: ['/static/css/tinymce.css', '/static/tinymce4/tinymce.css']

    custom_undo_redo_levels: 8,
    entity_encoding: 'raw',
//    element_format: "html",     // default is xhtml
    //schema: "html5-strict",   // default is html5

    // Don't validate the html. It will remove opengraph properties.
    // ... and maybe reformat the html?
    verify_html : false,

    // Allow OpenGraph elements
    //extended_valid_elements: "@[itemscope|itemtype|itemid|itemprop|content],div,span,time[datetime],h1[title],h2[title],h3[title]",

    // Don't touch/change url. (Do not convert to relative urls)
    convert_urls : false,
    // Can also do this. Might be more robust/safer.
    //document_base_url: document.location.origin + '/',
    //relative_urls : false,

    menubar: 'edit insert format table',
    // Default is: 'tools table format view insert edit'

    toolbar: 'undo redo | styleselect | bold italic forecolor | alignleft aligncenter alignright | bullist numlist outdent indent blockquote | link image | code',
    // Default is: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image'


    /** Plugins */

    plugins: ['image', 'link', 'paste', 'anchor', 'code', 'table', 'textcolor', 'visualblocks'],

    // @todo check out these:
    // save - adds a save button to toolbar
    // autosave - warn if unsaved data
    // wordcount
    // advlist  adds more advanced options to the ordered and unordered list
    // anchor - This plugin adds an anchor/bookmark button and menu
    // hr - menu item and button control that allows you to insert a hr
    // textpattern - markdown syntax

    code_dialog_width: 800,


    // Config: link plugin
    link_list: function (set_data) {
        var data = window._link_list_cache || null;
        if (data) { set_data (data); return; }

        get_json ('/tinymce/page-list/', function (data) {
            window._link_list_cache = data;
            set_data (data);
        });
    },


    // Config: image plugin
    image_list: [
	{title: 'Logo',         value: '/static/images/logo.png'},
	{title: 'Logo (liten)', value: '/static/images/logo-300.png'},
    ],
    image_advtab: true,

    file_browser_callback: function (field_name, url, type, win)
    {
	if (type != 'image') return;
	var el = $get ('tinymce-file-input');
	el.onchange = function (ev) {
	    //file = ev.target.files[0];
	    tinymce_upload (ev.target.form, $get (field_name));
	};
	el.click();
    }
});
