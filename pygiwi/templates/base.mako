<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/css/pygment.css">
<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script src="https://login.persona.org/include.js" type="text/javascript"></script>
<script type="text/javascript">${request.persona_js}</script>

</head>
<body>

##Hello ${user}
${request.persona_button}

<div id="wikilist">
available wikis: 
<ul>
%for  w in wikis:
<li><a href="${request.route_path('view_wiki', project=w, page='Home') }">${w}</a></li>
%endfor
</ul>
</div>

${next.body()}

</body>
</html>
