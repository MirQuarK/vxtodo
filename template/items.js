[
{% for item in items %}{
'id':'{{item.key.id}}',
'user':'{{item.user}}',
'title':'{{item.title|escape}}',
'content':"{{item.content|escape}}",
'color':'{{item.color}}',
'createtime':'{{item.createtime}}',
'endtime':'{{item.endtime}}',
'email':'{{item.email}}',
'remindtime':'{{item.remindtime}}',
'status':'{{item.status}}'
}{% if not forloop.last %},{% endif %}
{% endfor %}
]