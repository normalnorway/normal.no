"""
If you put this in a module that's loaded by default (your main urlconf
for instance), you'll have the tags and filters from your custom tag
module available in any template, without using {% load custom_tag_module %}
"""

# NOT IN USE

#from django import template
#template.add_to_builtins ('core.custom_tag_module')
#template.add_to_builtins ('project.app.templatetags.custom_tag_module')
