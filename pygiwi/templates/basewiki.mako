<%inherit file="base.mako" />


<div id="pygiwi-wiki">

  <div class="pygiwi-button">
    <a href=${request.route_path('wiki_home')}>wiki list</a>
    <a href=${request.route_path('wiki_project_home', project=project)}>Home page</a> 
 </div>

${next.body()}

</div>