<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/css/pygment.css">

</head>
<body>

available wikis: 
%for  w in wikis:
${w}
%endfor

${next.body()}

</body>
</html>
