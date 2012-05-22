/**
 * Dojo Rich Editor.
 *
 * Will convert all textareas to an rich text editor.
 *
 * http://livedocs.dojotoolkit.org/dijit/Editor
 * https://gist.github.com/868595
 * http://dojotoolkit.org/reference-guide/1.7/dijit/Editor.html
 */

dojo.require("dijit.Editor");

// Plugins
dojo.require("dijit._editor.plugins.FontChoice");
dojo.require("dijit._editor.plugins.LinkDialog");
dojo.require("dijit._editor.plugins.FullScreen");
dojo.require("dijit._editor.plugins.ViewSource");
dojo.require("dojox.editor.plugins.PrettyPrint");
dojo.require("dojox.editor.plugins.ShowBlockNodes");

// require(["dojo/parser", "dijit/Editor", "dijit/_editor/plugins/LinkDialog"]);
//dojo.require("dijit._editor.plugins.EnterKeyHandling"); // default
//dojo.require("dijit._editor.plugins.AlwaysShowToolbar");
//dojox.editor.plugins.
// ToolbarLineBreak, CollapsibleToolbar, AutoUrlLink
// Blockquote, InsertAnchor, LocalImage, SpellCheck

// @todo can load editor when textarea gets focused
// https://gist.github.com/1595530

dojo.ready (function()
{
    dojo.addClass (dojo.body(), "claro");

    dojo.query("textarea").instantiate (dijit.Editor,
    {
	styleSheets: "/static/css/editor.css",
	height: '400px',
//	width: '800px',	howto set width? css?
	
	plugins: [
	    dijit._editor.plugins.ViewSource,
	    'bold','italic','subscript','superscript','|','indent', 'outdent', 'justifyLeft', 'justifyCenter','justifyRight','|',
	    'insertImage',
	    'createLink',
	    '|',
	    'removeFormat',
	    'insertOrderedList', 'insertUnorderedList', 'insertHorizontalRule',
	    '|',
	    'fontSize', 'formatBlock',
	    'fullScreen',
	    'showBlockNodes',
	],

	extraPlugins: [
	    { name:'dijit._editor.plugins.EnterKeyHandling',
		blockNodeForEnter:'P'
	    },

//	    dojox.editor.plugins.ShowBlockNodes,

	    // Headless plugins
	    { name: 'prettyprint',
		indentBy: 2,
		lineLength: 80,
		entityMap: [['<', 'lt'],['>', 'gt']],
	    },
	],
    });
});
