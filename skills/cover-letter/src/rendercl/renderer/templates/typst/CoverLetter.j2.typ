#import "@preview/letterloom:3.0.0": *

#show: letterloom.with(
  from-name: [*{{ from_name }}*],
  from-address: [
{{ from_address_lines }}
  ],
  to-name: {% if to_name %}"{{ to_name }}"{% else %}none{% endif %},
  to-address: [
{{ to_address_lines }}
  ],
  date: "{{ date }}",
  required-fields: ("from-name", "from-address", "to-address", "date"{% if to_name %}, "to-name"{% endif %}),
  main-font: "{{ font_family }}",
  main-font-size: {{ font_size }},
  paper-size: "{{ paper_size }}",
  margins: {{ margins }},
  link-color: black,
)

#set par(justify: true)

#v(0.5em)
{{ salutation }}

{{ body }}

#v(0.5em)
{{ closing }}

{{ from_name }}
