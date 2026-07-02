# Stack: WordPress + Elementor

- Changes via child theme or custom plugin, never edit parent theme files
- No Trustpilot widgets or ratings anywhere on M3M properties; Google reviews only
- Test on mobile viewport before declaring layout work done
- Document any plugin added and why

## Code standards

- Enqueue all scripts and styles with wp_enqueue_script/wp_enqueue_style; never hardcode tags in templates
- Prefix every custom function, hook, shortcode, and option to avoid collisions
- Sanitize all input, escape all output (esc_html, esc_attr, esc_url, wp_kses); nonces on every form and AJAX handler
- Database access through WP APIs (options, post meta, WP_Query, $wpdb->prepare); no raw SQL string concatenation
- Never modify WordPress core

## Elementor specifics

- Global styles (colors, fonts, spacing) live in Elementor site settings or theme tokens; avoid per-widget inline style drift
- Custom widgets and dynamic tags go in a custom plugin, not the theme
- Reusable sections as templates, not copy-pasted blocks

## Operations

- All changes hit a staging or local environment before a live site; never edit live directly
- Back up (files + database) before plugin, theme, or core updates on live sites
- Keep the plugin count minimal; deactivated plugins get removed, and each remaining one is documented

## References

- docker/awesome-compose (https://github.com/docker/awesome-compose): ready-made WordPress + MySQL compose samples for spinning up local dev environments
