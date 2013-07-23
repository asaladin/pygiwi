<html>
<head>
<link rel="stylesheet" type="text/css" href="${request.static_path('pygiwi:static/css/pygment.css')}" >
<link rel="stylesheet" type='text/css' href="${request.static_path('pygiwi:static/css/pygiwi.css')}" >
<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script src="https://login.persona.org/include.js" type="text/javascript"></script>
<script type="text/javascript">${request.persona_js}</script>

</head>
<body>

In order to edit this page, you must first login. Please click on the button below: <br />

${request.persona_button}

</body>
</html>
