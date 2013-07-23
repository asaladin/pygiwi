<%inherit file="basewiki.mako" />


    <div id="format-desc">
	This wiki page is in <span id="format">${format}</span>
    </div>

    <div class="pygiwi-button">
	<a id="edit" href="${edit_url}">Edit page</a>
    </div>

    <div id="wiki-content">
	${content|n}
    </div>
