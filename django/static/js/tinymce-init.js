tinymce.init ({
    selector: '#id_content',
//    selector: 'textarea.tinymce',
//    selector: 'textarea.vLargeTextField',
    width: 800,
    height: 450,
    resize: 'both',
    custom_undo_redo_levels: 8,

    menubar: 'edit insert format table',
    //menubar: 'tools table format view insert edit',	// default

    toolbar: 'undo redo | styleselect | bold italic forecolor | alignleft aligncenter alignright | bullist numlist outdent indent blockquote | link image | code',
    //toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',	// defaults

    plugins: ['image', 'link', 'paste', 'anchor', 'code', 'table', 'textcolor'],

    /* Note: will override defaults
    // Defaults: http://www.tinymce.com/wiki.php/Configuration:style_formats
    style_formats: [
	{title: 'Ingress', block: 'div', classes: 'ingress'},
	{title: 'Tittel', block: 'h1', styles: {color: 'green'}},
	{title: 'Row border', selector: 'tr', classes: 'foobar'},
	// @note selector can be complex css selector. e.g., odd rows in
	// a table.
    ],
    */

    link_list: [
	{title: 'Blogg',	value: 'http://blogg.normal.no'}, 
	{title: 'Facebook',	value: 'https://www.facebook.com/NormalNorway'}, 
	{title: 'Youtube',	value: 'http://www.youtube.com/user/normalnorway'}, 
	{title: 'Nyhetsbrev',	value: 'http://eepurl.com/S3rFH'}, 
	{title: 'Donér',	value: 'alert("todo")'}, 
    ],

    /** Image plugin */
    image_list: [ 
	{title: 'Logo', value: 'http://normal.no/logo.png'}, 
    ],
    image_advtab: true,
    file_browser_callback: function (field_name, url, type, win) {
	alert ('fixme');
    }
});
