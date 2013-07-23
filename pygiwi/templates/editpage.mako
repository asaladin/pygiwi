<%inherit file="basewiki.mako" />

<%block name='header'>
<script type="text/javascript" src="${request.static_path('pygiwi:static/markitup/1.1.14/markitup/jquery.markitup.js')}"></script>
<script type="text/javascript" src="${request.static_path('pygiwi:static/markitup/1.1.14/markitup/sets/markdown/set.js')}"></script>

<link rel="stylesheet" type="text/css" href="${request.static_path('pygiwi:static/markitup/1.1.14/markitup/skins/markitup/style.css')}" />
<link rel="stylesheet" type="text/css" href="${request.static_path('pygiwi:static/markitup/1.1.14/markitup/sets/markdown/style.css')}" />
</%block>

<script type="text/javascript" >
   $(document).ready(function() {
      $("#markdown").markItUp(mySettings);
   });
</script>


<p>Tip: you can click on the rightmost button to see a preview before submitting.</p>

<form name="theform" method="post">
<input type="hidden" name="lastcommitid" value="${commit_id}">
<textarea id="markdown" name="content" rows="30" cols="100">${content}</textarea> <br />
<input type="submit" />
</form>

