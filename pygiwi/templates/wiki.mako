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
       
#format {
          background-color: #f3f3f3;
        }

</style>


<a href=${request.route_url('wiki_home')}>wiki list</a> <br /> <br />



<div id="format-desc">
This wiki is in <span id="format">${format}</span>
</div>

<a id="edit" href="${edit_url}">edit page</a>

<div id="wiki-content">
${content|n}
</div>