<%inherit file="base.mako" />


<div id="pygiwi-wiki">

  <div class="pygiwi-button">
    <a href=${request.route_url('wiki_home')}>wiki list</a>
    <a href=${request.route_url('wiki_project_home', project=project)}>Home page</a> 
 </div>


    <div id="format-desc">
	This wiki page is in <span id="format">${format}</span>
    </div>

    <div class="pigiwi-button">
	<a id="edit" href="${edit_url}">Edit page</a>
    </div>

    <div id="wiki-content">
	${content|n}
    </div>

</div>