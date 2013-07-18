<%inherit file="base.mako" />

<form name="theform" method="post">
<input type="hidden" name="lastcommitid" value="${commit_id}">
<textarea name="content" rows="30" cols="100">${content}</textarea> <br />
<input type="submit" />
</form>