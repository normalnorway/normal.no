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


function _foo (ev)
{
    var editor = tinymce.activeEditor;
//    console.log (editor);

    var node = editor.selection.getNode();

    if (node.nodeName != 'IMG') {
        alert ('You must select an image first!');
        return;
    }

    // @todo check if already contains caption
    // editor.dom.getParent (node, '.wp-caption');
    // @todo mceAddUndoLevel

    //el = tinymce.dom.createFragment ('<figure></figure>');
//    el = editor.dom.create ('figure');
//    caption = editor.dom.create ('figcaption', {}, 'Bla, bla, bla. For et flott bilde');

    wrapper = editor.dom.create ('div', {}, 'Hello World!');

    wrapper.appendChild (node.cloneNode (false));

    editor.dom.replace (wrapper, node);

    return;

    el.appendChild (node);
    el.appendChild (caption);
    console.log (el);

    editor.dom.replace (el, node);
}


// Django TinyMCE4 namespace
window.djangomce =
{
//    config: {},
//    cache: {},
//    upload: function (form, output) { ... },

    _setup: function (editor) {
        editor.addMenuItem ('code', {context: 'tools'});
        //editor.addMenuItem ('visualblocks', {context: 'tools'});

        editor.addMenuItem ('foo', { text: 'Foo', context: 'tools', onclick: _foo, });

//        editor.addMenuItem ('myitem', {
//            text: 'Testing', context: 'tools', onclick: function() {
//                txt = prompt('Bildetekst: ');
//                editor.insertContent (txt);
//        }});
    },
};




// @todo only install if needed?
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
 * - need way to override default config per widget?
 */

tinymce.init ({
    selector: 'textarea.tinymce',
    width: 730,
    height: 550,
    resize: 'both',

    setup: djangomce._setup,

    code_dialog_width: 800,

    content_css: '/static/css/tinymce.css',

    custom_undo_redo_levels: 12,

    entity_encoding: 'raw',
    //element_format: "html",     // default is xhtml

    // Does schema have any effect with verify_html=false?
    //schema: "html5-strict",   // default is html5

    // Don't validate the html. It will remove opengraph properties.
    // ... and probably reformat the html?
    verify_html: false,

    // Allow OpenGraph elements
    // Q: Will override the default list of allowed attributes?
    //extended_valid_elements: "@[itemscope|itemtype|itemid|itemprop|content],div,span,time[datetime],h1[title],h2[title],h3[title]",

    // Need this to get absolute urls in image plugin (upload)
    convert_urls : false,
    // this might also fix it:
    // keep convert_urls at its default (true) + relative_urls = false
    // Use absolute urls. (URLs returned from the MCFileManager)
    //relative_urls : false,

    // @todo filter all javascript?
    // invalid_elements: '@[onclick|ondblclick|onmousedown|onmouseup|onmouseover|onmousemove|onmouseout|onkeypress|onkeydown|onkeyup],script,input,select,option,button,textarea,form',

    // @todo test
    // statusbar : false,
    // indentation
    // valid_classes
    // body_id	    // use this id for TinyMCE specific overrides in content_css
    //toolbar: "insertfile
    //preview_styles
    //fontsizeselect

    // Custom class to be added to anchors or tables, since these are
    // invisible by default. Note: visual=true (default) adds dashed border.
    //visual_table_class // can use to style all tinymce tables differently
    visual_anchor_class: 'anchor',


    // http://www.tinymce.com/wiki.php/Configuration:style_formats
    // @todo use names like div.caption, div.clear, hr.fancy?
//    style_formats_merge: true,
    style_formats: [

        {title: "Headers", items: [
            {title: "Header 1", format: "h1"},
            {title: "Header 2", format: "h2"},
            {title: "Header 3", format: "h3"},
            {title: "Header 4", format: "h4"},
        ]},

        {title: "Inline", items: [
            // Note: removed: bold,italic,underline,strikethrough
            {title: "Superscript", icon: "superscript", format: "superscript"},
            {title: "Subscript", icon: "subscript", format: "subscript"},
            {title: "Code", icon: "code", format: "code"},
        ]},

        {title: "Blocks", items: [
            {title: "Paragraph", format: "p"},
            {title: "Blockquote", format: "blockquote"},
            //{title: "Div", format: "div"},
            {title: "Pre-formatted", format: "pre"},
            // @todo address?, html5 block elements
        ]},

        // Site styles / semantic classes from classes.less

        // Inline styles (acts on word or selection)
        {title: "Strong", inline: 'span', classes: 'strong'},
        {title: "Smaller", inline: 'span', classes: 'smaller'},
        {title: "Larger", inline: 'span', classes: 'larger'},
//        {title: "Highlight", inline: 'span', classes: 'highlight'},
//        {title: "Shade", inline: 'span', classes: 'grey'},

        // uthev, sitat (blockquote & inline?)

        // Paragraph styles (block styles)
        {title: "Ingress", block: 'p', classes: 'ingress'},
        {title: "Faktaboks", block: 'div', wrapper: true, classes: 'faktaboks'},
//        {title: 'Section', block: 'section', wrapper: true, merge_siblings: false},

        {title: 'Table: align top', selector: 'td', classes: 'valign-top'},
//        {title: 'Image left', selector: 'img', styles: {'float': 'left'}},
//        {title: 'Image right', selector: 'img', styles: {'float': 'right'}},
//        {title: "Clear floats", wrapper: true, classes: 'clear'},

        // rename "remove style classes"?
        {title: 'No style', selector: '*', attributes: {'class' : 'no-style'}},
    ],


    // Toolbar controls & Menu controls:
    // http://www.tinymce.com/wiki.php/Controls

    // http://www.tinymce.com/wiki.php/Configuration:menu
    //menubar: 'edit insert format table view tools',

    menu: {
        edit: { title: 'Edit', items:
            'undo redo | cut copy paste pastetext | selectall searchreplace'},
        insert: { title: 'Insert', items:
            'image link media | anchor | hr nonbreaking insertdatetime'},
        format: { title: 'Format', items:
            'bold italic underline strikethrough superscript subscript | formats | removeformat'},
        table: { title: 'Table', items:
            'inserttable tableprops deletetable | cell row column'},
        tools: { title: 'Tools', items:
            'code visualblocks charmap fullscreen foo'},
    },

    toolbar1: 'undo redo | styleselect | bold italic forecolor | ' +
             'alignleft aligncenter alignright | ' +
             'bullist numlist outdent indent blockquote | ' +
             'link image | code',

    toolbar2: 'formatselect fontsizeselect removeformat ' +
              'preview fullscreen | template',

    /** Plugins */

    plugins: [
        'image', 'link', 'paste', 'anchor', 'code', 'table', 'textcolor',
        'visualblocks', 'nonbreaking', 'insertdatetime', 'hr', 'media',
        'searchreplace', 'charmap', 'paste',
        'preview', 'fullscreen', 'template',
    ],

    // paste - paste from word cleanup plugin
    //paste_as_text: true,    // force paste as text always
    //paste_preprocess: function (plugin, args) { args.content += 'test'; },
    //paste_postprocess: preprocess: but uses dom (not string)
    //paste_word_valid_elements: "b,strong,i,em,h1,h2"

    insertdatetime_formats: ['%d.%m.%Y', '%Y-%m-%d'],

    // @todo check out these:
    // autosave - warn if unsaved data
    // wordcount
    // advlist  adds more advanced options to the ordered and unordered list
    // textpattern - markdown syntax
    // template (supports snippets)


    // Config: link plugin
    // Fetch list of flat pages from django
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

    // Handle file upload
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
