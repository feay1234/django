from django import template

register = template.Library()
@register.filter  
def check_request(user, user_list):
	for i in user_list:
		if user == i.sender or user == i.receiver:
			return True
	return False