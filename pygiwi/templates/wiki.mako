<%inherit file="base.mako" />

<style type='text/css'>
#wiki-content {
       width:830px;
       background-color:white;
       padding-left:5px;
       padding-right:5px;
       border: 1px dotted grey;
       margin: 0 15px 0 13px;
    }

</style>

<div id="wiki-content">
${content|n}
</div>