/**
 * Dojo Rich Editor.
 *
 * Will convert all textareas to an rich text editor.
 *
 * http://dojotoolkit.org/reference-guide/1.7/dijit/Editor.html
 * http://livedocs.dojotoolkit.org/dijit/Editor
 * https://gist.github.com/868595
 *
 * REQUIRES: window.djangovar.STATIC_URL
 *
 * @see /static/css/editor.css
 */

// @todo menu to apply custom styles! <div style="ingress">
// @todo createLink: remove target
// @todo possible to disable image resizing?

// @todo only load editor when textarea gets focused?
// https://gist.github.com/1595530


// Modern (async) way: http://livedocs.dojotoolkit.org/loader/amd
require([
//    "dojo/parser",
    "dijit/Editor",

    // Plugins
    "dijit/_editor/plugins/FontChoice",
    "dijit/_editor/plugins/LinkDialog",	// enhances createLink
    "dijit/_editor/plugins/FullScreen",
    "dijit/_editor/plugins/ViewSource",

    "dojox/editor/plugins/LocalImage",
    "dojox/editor/plugins/ShowBlockNodes",

    // Headless plugins
    "dojox/editor/plugins/PrettyPrint",
    "dojox/editor/plugins/ToolbarLineBreak",

], init_dojo_editor);	// Second arg => ready function


function init_dojo_editor()
{
    dojo.addClass (dojo.body(), "claro");   // style

    dojo.query("textarea").instantiate (dijit.Editor,
    {
	styleSheets: window.djangovar.STATIC_URL + "/css/editor.css",
	height: '480px',    // can not be set in css(?) [iframe]

	// Toolbar
	plugins: [
	    'bold', 'italic', 'underline', 'strikethrough', 'subscript', 'superscript', '|',
	    'insertOrderedList', 'insertUnorderedList', 'indent', 'outdent', '|',
	    'justifyLeft', 'justifyCenter', 'justifyRight', '|',
//	    'createLink', 'insertImage', 'insertHorizontalRule', '|',
	    'createLink',
		{ name: 'LocalImage', uploadable: true, uploadUrl: '/files/upload' },
		'insertHorizontalRule', '|',
	    'undo', 'redo', '|', 
	    'fullScreen',
	    '||',
	    'formatBlock', 'fontSize', 'removeFormat', '|',
	    /*
	    {
		name:    'dijit._editor.plugins.FontChoice',
		command: 'formatBlock',
		custom:  ["p", "h1", "h2", "h3", "pre", "blockquote"],
		// did not work :(
		//custom:  ["p style='ingress'", "h1", "h2", "h3", "pre"],
	    },
	    */
	    /*
	    {
		name:    'dijit._editor.plugins.FontChoice',
		command: 'fontName',
		generic: true,
//		custom:  ['serif', 'sans-serif', 'mono'],
	    },
	    */
	    'showBlockNodes', 'viewSource',
	],
//	plugins: [{name:'dijit._editor.plugins.FontChoice', command:'fontName', custom:['Verdana','Myriad','Garamond']}],

	// Headless plugins
	extraPlugins: [
	    {
		name: 'dijit._editor.plugins.EnterKeyHandling',
//		name: 'EnterKeyHandling', // does not work
		blockNodeForEnter: 'P'
	    },
	    {
		name: 'PrettyPrint',
		indentBy: 2,
		lineLength: 80,
		entityMap: [['<', 'lt'],['>', 'gt']],
	    },
	],
    });
};




/** Other interesting plugins

dojox.editor.plugins:	(note: some are not stable)
  AutoUrlLink, Blockquote, InsertAnchor, SpellCheck

  Breadcrumb	status bar show the HTML node nesting, and menu
                for each element to edit (delete, move to start, etc)
  PageBreak	insert pagebreak for printing
  Preview	preview with other (site) stylesheet
  StatusBar	allows users to resize the editor! (experimental)

"dojox/editor/plugins/CollapsibleToolbar",
Weakness: not possible to start in the collapsed state.

"dojox/editor/plugins/SafePaste",
Can use this to disable direct paste, and choose a list
of tags to strip. (But has no button / headless)
@todo need paste-as-plain-text button
*/




/* Old way to do it
dojo.require("dijit.Editor");

// Plugins
dojo.require("dijit._editor.plugins.FontChoice");
dojo.require("dijit._editor.plugins.LinkDialog");
dojo.require("dijit._editor.plugins.FullScreen");
dojo.require("dijit._editor.plugins.ViewSource");
dojo.require("dojox.editor.plugins.PrettyPrint");
dojo.require("dojox.editor.plugins.ShowBlockNodes");
dojo.require("dojox.editor.plugins.ToolbarLineBreak");

// Default loaded plugins:
// dijit._editor.plugins.EnterKeyHandling

dojo.ready (init_dojo_editor);
*/
