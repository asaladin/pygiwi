<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/css/pygment.css">
<link rel="stylesheet" type='text/css' href="/static/css/pygiwi.css">
<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script src="https://login.persona.org/include.js" type="text/javascript"></script>
<script type="text/javascript">${request.persona_js}</script>

</head>
<body>


 %for m in request.session.pop_flash('error'):
    <div class="alert alert-error">
       ${m}
    </div>
 %endfor

 
    %for m in request.session.pop_flash():
    <div class="alert alert-success">
       ${m}
    </div>
    %endfor
 
%if request.user is not None:
<span style='float:right'>Hello ${request.user} <a href='.' id='signout'>logout</a>  </span>

%else:
${request.persona_button}
%endif

<div class="pygiwi-body">
${next.body()}
</div>

</body>
</html>
