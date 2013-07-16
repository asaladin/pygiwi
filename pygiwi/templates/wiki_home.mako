<%inherit file="base.mako" />

List of available wikis:

<div id="wikilist">
<ul>
%for  w in wikis:
<li><a href="${request.route_path('view_wiki', project=w, page='Home') }">${w}</a></li>
%endfor
</ul>
</div>