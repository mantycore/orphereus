# -*- coding: utf-8 -*-

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title id='title'>Orphereus: experimental webtop</title>

    <link rel="stylesheet" type="text/css" href="${g.OPT.staticPathWeb}js/ext/resources/css/ext-all.css" />
    <link rel="stylesheet" type="text/css" href="${g.OPT.staticPathWeb}js/ext/examples/desktop/css/desktop.css" />

    <!-- overrides to base library -->


    <!-- ** Javascript ** -->
    <!-- ExtJS library: base/adapter -->
    <script type="text/javascript" src="${g.OPT.staticPathWeb}js/ext/adapter/ext/ext-base.js"></script>
    <!-- ExtJS library: all widgets -->
    <script type="text/javascript" src="${g.OPT.staticPathWeb}js/ext/ext-all-debug.js"></script>

    <!-- overrides to library -->

    <!-- extensions -->
    <script type="text/javascript" src="${g.OPT.staticPathWeb}js/ext/examples/desktop/js/StartMenu.js"></script>
    <script type="text/javascript" src="${g.OPT.staticPathWeb}js/ext/examples/desktop/js/TaskBar.js"></script>

    <script type="text/javascript" src="${g.OPT.staticPathWeb}js/ext/examples/desktop/js/Desktop.js"></script>
    <script type="text/javascript" src="${g.OPT.staticPathWeb}js/ext/examples/desktop/js/App.js"></script>
    <script type="text/javascript" src="${g.OPT.staticPathWeb}js/ext/examples/desktop/js/Module.js"></script>
    <script type="text/javascript" src="${g.OPT.staticPathWeb}js/ext/examples/desktop/sample.js"></script>

    <!-- page specific -->
<script type="text/javascript">
// Path to the blank image should point to a valid location on your server
Ext.BLANK_IMAGE_URL = '${g.OPT.staticPathWeb}js/ext/resources/images/default/s.gif';

MyDesktop.PluginsWindow = Ext.extend(Ext.app.Module, {
    id:'plugins-win',
    init : function(){
        this.launcher = {
            text: 'Plugins Window',
            iconCls:'icon-grid',
            handler : this.createWindow,
            scope: this
        }
    },

    createWindow : function(){
        var desktop = this.app.getDesktop();
        var win = desktop.getWindow('plugins-win');
        if(!win){
var PluginsDataStore;         // this will be our datastore
var PluginsColumnModel;       // this will be our columnmodel
var PluginsEditorGrid;
var PluginsListingWindow;

  PluginsDataStore = new Ext.data.Store({
      id: 'PluginsDataStore',
      proxy: new Ext.data.HttpProxy({
                url: '${h.url_for('hsAjPluginsList')}',      // File to connect to
                method: 'GET'
            }),
            //baseParams:{task: "LISTING"}, // this parameter asks for listing
       reader: new Ext.data.JsonReader({
                  // we tell the datastore where to get his data from
        root: 'results',
        totalProperty: 'total',
        id: 'id'
      },[
        {name: 'id', type: 'string', mapping: 'id'},
        {name: 'descr', type: 'string', mapping: 'descr'},
        {name: 'deps', type: 'string', mapping: 'deps'},
        {name: 'namespace', type: 'string', mapping: 'namespace'},
        {name: 'file', type: 'string', mapping: 'file'},
      ]),
      sortInfo:{field: 'id', direction: "ASC"}
    });

PluginsColumnModel = new Ext.grid.ColumnModel(
    [{
        header: 'Id',
        readOnly: true,
        dataIndex: 'id',
        width: 100,
        hidden: false
      },
      {
        header: 'Description',
        readOnly: true,
        dataIndex: 'descr',
        width: 300,
        hidden: false
      },
      {
        header: 'File name',
        readOnly: true,
        dataIndex: 'file',
        width: 150,
        hidden: false
      },
      {
        header: 'Namespace',
        readOnly: true,
        dataIndex: 'namespace',
        width: 250,
        hidden: false
      },
      {
        header: 'Dependencies',
        readOnly: true,
        dataIndex: 'deps',
        width: 100,
        hidden: false
      },
  ]
    );
    PluginsColumnModel.defaultSortable= true;

 PluginsEditorGrid =  new Ext.grid.GridPanel({
      id: 'PluginsListingEditorGrid',
      store: PluginsDataStore,     // the datastore is defined here
      cm: PluginsColumnModel,      // the columnmodel is defined here
      enableColLock:false,
      clicksToEdit:0,
      stripeRows: true,
      selModel: new Ext.grid.RowSelectionModel({singleSelect:false})
    });


            win = desktop.createWindow({
                id: 'plugins-win',
                title: 'Loaded Orphereus plugins',
                width:1000,
                height:500,
                iconCls: 'icon-grid',
                shim:false,
                animCollapse:false,
                constrainHeader:true,

                layout: 'fit',
                items: PluginsEditorGrid
            });

  PluginsDataStore.load();      // Load the data
        }
        win.show();
    }
});


/*

Ext.onReady(function() {
var PluginsDataStore;         // this will be our datastore
var PluginsColumnModel;       // this will be our columnmodel
var PluginsEditorGrid;
var PluginsListingWindow;

  PluginsDataStore = new Ext.data.Store({
      id: 'PluginsDataStore',
      proxy: new Ext.data.HttpProxy({
                url: '${h.url_for('hsAjPluginsList')}',      // File to connect to
                method: 'GET'
            }),
            //baseParams:{task: "LISTING"}, // this parameter asks for listing
       reader: new Ext.data.JsonReader({
                  // we tell the datastore where to get his data from
        root: 'results',
        totalProperty: 'total',
        id: 'id'
      },[
        {name: 'id', type: 'string', mapping: 'id'},
        {name: 'descr', type: 'string', mapping: 'descr'},
        {name: 'deps', type: 'string', mapping: 'deps'},
        {name: 'namespace', type: 'string', mapping: 'namespace'},
        {name: 'file', type: 'string', mapping: 'file'},
      ]),
      sortInfo:{field: 'id', direction: "ASC"}
    });

PluginsColumnModel = new Ext.grid.ColumnModel(
    [{
        header: 'Id',
        readOnly: true,
        dataIndex: 'id',
        width: 100,
        hidden: false
      },
      {
        header: 'Description',
        readOnly: true,
        dataIndex: 'descr',
        width: 300,
        hidden: false
      },
      {
        header: 'File name',
        readOnly: true,
        dataIndex: 'file',
        width: 150,
        hidden: false
      },
      {
        header: 'Namespace',
        readOnly: true,
        dataIndex: 'namespace',
        width: 250,
        hidden: false
      },
      {
        header: 'Dependencies',
        readOnly: true,
        dataIndex: 'deps',
        width: 100,
        hidden: false
      },
  ]
    );
    PluginsColumnModel.defaultSortable= true;

 PluginsEditorGrid =  new Ext.grid.GridPanel({
      id: 'PluginsListingEditorGrid',
      store: PluginsDataStore,     // the datastore is defined here
      cm: PluginsColumnModel,      // the columnmodel is defined here
      enableColLock:false,
      clicksToEdit:0,
      stripeRows: true,
      selModel: new Ext.grid.RowSelectionModel({singleSelect:false})
    });

  PluginsListingWindow = new Ext.Window({
      id: 'PluginsListingWindow',
      title: 'Loaded Orphereus plugins',
      closable:true,
      width:1000,
      height:350,
      plain:true,
      layout: 'fit',
      items: PluginsEditorGrid  // We'll just put the grid in for now...
    });

  PluginsDataStore.load();      // Load the data
  //PluginsListingWindow.show();   // Display our window

});*/
</script>

</head>
<body scroll="no">

<div id="x-desktop">
    <a href="http://extjs.com" target="_blank" style="margin:5px; float:right;"><img src="images/powered.gif" /></a>

    <dl id="x-shortcuts">
        <dt id="grid-win-shortcut">
            <a href="#"><img src="images/s.gif" />
            <div>Grid Window</div></a>
        </dt>
    </dl>
</div>

<div id="ux-taskbar">
  <div id="ux-taskbar-start"></div>
  <div id="ux-taskbuttons-panel"></div>
  <div class="x-clear"></div>
</div>

</body>
</html>
