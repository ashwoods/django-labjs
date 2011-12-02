Django Lab.js
=================

Django templatetags to Labify your scripts: http://labjs.com/

Installation
============

#TODO

Usage
=====

{% labjs %}
<script type="text/javascript" src="src/myjs.js" />
{% wait %}
<script type="text/javascript">
... inline script
<script>

{% endlabjs %}


{% runlab %}
{% endrunlab %}
