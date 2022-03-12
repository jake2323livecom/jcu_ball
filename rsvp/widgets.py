from django.forms import RadioSelect


class HorizontalRadioSelect(RadioSelect):
    template_name = "rsvp/horizontal_radios.html"
    option_template_name = "rsvp/horizontal_option.html"
