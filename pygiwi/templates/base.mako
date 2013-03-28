<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/css/pygment.css">

</head>
<body>

<div id="wikilist">
available wikis: 
<ul>
%for  w in wikis:
<li>${w}</li>
%endfor
</ul>
</div>

${next.body()}

</body>
</html>
