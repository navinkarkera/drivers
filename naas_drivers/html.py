from htmlBuilder import tags, attributes
import IPython.core.display

#  https://litmus.com/community/templates/31-accessible-product-announcement-email
base_style = """
/* CLIENT-SPECIFIC STYLES */
body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
img { -ms-interpolation-mode: bicubic; }

/* RESET STYLES */
img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }
table { border-collapse: collapse !important; }
body { height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }

/* iOS BLUE LINKS */
a[x-apple-data-detectors] {
    color: inherit !important;
    text-decoration: none !important;
    font-size: inherit !important;
    font-family: inherit !important;
    font-weight: inherit !important;
    line-height: inherit !important;
}

/* GMAIL BLUE LINKS */
u + #body a {
    color: inherit;
    text-decoration: none;
    font-size: inherit;
    font-family: inherit;
    font-weight: inherit;
    line-height: inherit;
}

/* SAMSUNG MAIL BLUE LINKS */
#MessageViewBody a {
    color: inherit;
    text-decoration: none;
    font-size: inherit;
    font-family: inherit;
    font-weight: inherit;
    line-height: inherit;
}

/* These rules set the link and hover states, making it clear that links are, in fact, links. */
/* Embrace established conventions like underlines on links to keep emails accessible. */
a { color: #B200FD; font-weight: 600; text-decoration: underline; }
a:hover { color: #000000 !important; text-decoration: none !important; }
a.button:hover { color: #ffffff !important; background-color: #000000 !important; }

/* These rules adjust styles for desktop devices, keeping the email responsive for users. */
/* Some email clients don't properly apply media query-based styles, which is why we go mobile-first. */
@media screen and (min-width:600px) {
    h1 { font-size: 48px !important; line-height: 48px !important; }
    .intro { font-size: 24px !important; line-height: 36px !important; }
}
"""

basic_font = "'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'"  # noqa: E501
table_ie9 = """
<!--[if (gte mso 9)|(IE)]>
<table cellspacing="0" cellpadding="0" border="0" width="720" align="center" role="presentation"><tr><td>
<![endif]-->
"""

table_ie9_close = """
<!--[if (gte mso 9)|(IE)]>
</td></tr></table>
<![endif]-->
"""


class Html:
    """ HTML generator lib"""

    def address(self, title, content):
        return tags.Address(
            attributes.InlineStyle(
                font_size="16px",
                font_style="normal",
                font_weight="400",
                line_height="24px",
            ),
            tags.Strong(tags.Text(title)),
            tags.Text(content),
        )

    def link(self, link, title):
        return tags.A(
            attributes.Href(link),
            attributes.InlineStyle(color="#B200FD", text_decoration="underline"),
            tags.Text(title),
        )

    def header(self, *elems):
        return tags.Header(*elems)

    def footer(self, text, first=None, *elems):
        one = [
            attributes.InlineStyle(
                font_size="16px",
                font_weight="400",
                line_height="24px",
                margin_top="48px",
            ),
            tags.Text(text),
            first,
        ]
        return tags.Footer(tags.P(one), *elems)

    def info(self, *elems):
        return tags.Div(
            attributes.InlineStyle(
                background_color="ghostwhite",
                border_radius="4px",
                padding="24px 48px",
            ),
            *elems
        )

    def space(self):
        return tags.Br()

    def table(self, *sentences):
        elems = [
            attributes.InlineStyle(
                column_count="2", line_height="2", text_align="left"
            ),
        ]
        for sentence in sentences:
            if isinstance(sentence, str):
                elems.append(tags.Text(sentence))
                elems.append(tags.Br())
            else:
                elems.append(sentence)
        return tags.P(elems)

    def logo(self, src, link=None, name="Logo"):
        if src is None:
            return None
        elems_img = [
            attributes.Src(src),
            attributes.Height(80),
            attributes.Width(80),
            {"name": "alt", "value": name},
        ]
        if link:
            return tags.A(attributes.Href(link), tags.Center(tags.Img(elems_img)))
        else:
            return tags.Center(tags.Img(elems_img))

    def cover(self, src, link=None, name="Cover"):
        if src is None:
            return None
        elems_img = [
            attributes.Src(src),
            attributes.Height(80),
            attributes.Width(600),
            {"name": "border", "value": 0},
            attributes.InlineStyle(
                border_radius="4px",
                display="block",
                max_width="100%",
                min_width="100px",
                width="100%",
            ),
            {"name": "alt", "value": name},
        ]
        if link:
            return tags.A(attributes.Href(link), tags.Img(elems_img))
        else:
            return tags.Img(elems_img)

    def title(self, title, subtitle=None):
        return tags.H1(
            attributes.InlineStyle(
                color="#000000",
                font_size="32px",
                font_weight="800",
                line_height="32px",
                margin="48px 0",
                text_align="center",
            ),
            tags.Text(title),
            tags.Br(),
            (
                tags.Span(
                    attributes.InlineStyle(font_size="24px", font_weight="600"),
                    tags.Text(subtitle),
                )
                if subtitle
                else None
            ),
        )

    def subtitle(self, subtitle):
        return tags.H2(
            attributes.InlineStyle(
                color="#000000",
                font_size="28px",
                font_weight="600",
                line_height="32px",
                margin="48px 0 24px 0",
                text_align="center",
            ),
            tags.Text(subtitle),
        )

    def button(self, text, link, color="#ffffff", background_color="#B200FD"):
        return tags.Center(
            tags.Div(
                attributes.InlineStyle(margin="48px 0"),
                tags.A(
                    attributes.Class("button"),
                    attributes.Href(link),
                    attributes.InlineStyle(
                        background_color=background_color,
                        color=color,
                        border_radius="4px",
                        display="inline-block",
                        font_family="sans-serif",
                        font_size="18px",
                        font_weight="bold",
                        line_height="60px",
                        text_align="center",
                        text_decoration="none",
                        width="300px",
                        _webkit_text_size_adjust="none",
                    ),
                    tags.Text(text),
                ),
            )
        )

    def text(self, text, *agrs):
        return tags.P(*agrs, tags.Text(text))

    def template_basic(
        self,
        title,
        sub_title,
        content,
        logo=None,
        cover=None,
        table=None,
        button=None,
        footer=None,
    ):
        return [
            self.header(logo, self.title(title)),
            tags.Main(
                cover,
                self.subtitle(sub_title),
                tags.P(tags.Text(content) if isinstance(content, str) else content),
                table,
                button,
            ),
            footer,
        ]

    def generate(self, title, *content, display=True):
        html = tags.Html(
            attributes.Lang("en"),
            tags.Head(
                tags.Title(tags.Text(title)),
                tags.Meta(
                    attributes.HttpEquiv("Content-Type"),
                    attributes.Content("text/html; charset=utf-8"),
                ),
                tags.Meta(
                    attributes.HttpEquiv("Content-Type"),
                    attributes.Content("width=device-width, initial-scale=1"),
                ),
                tags.Meta(
                    attributes.Name("viewport"),
                    attributes.Content("width=device-width, initial-scale=1"),
                ),
                tags.Meta(
                    attributes.HttpEquiv("X-UA-Compatible"),
                    attributes.Content("IE=edge"),
                ),
                tags.Style(tags.Text(base_style)),
            ),
            tags.Body(
                attributes.InlineStyle(margin="0 !important", padding="0 !important"),
                tags.Div(
                    attributes.InlineStyle(
                        display="none", max_height="0", overflow="hidden"
                    )
                ),
                tags.Div(
                    attributes.InlineStyle(
                        display="none", max_height="0", overflow="hidden"
                    ),
                    tags.Text("&nbsp;‌" * 240),
                ),
                tags.Text(table_ie9),
                tags.Div(
                    {"name": "role", "value": "article"},
                    {"name": "aria-label", "value": title},
                    attributes.Lang("en"),
                    attributes.InlineStyle(
                        background_color="white",
                        color="#2b2b2b",
                        font_size="18px",
                        font_weight="400",
                        line_height="28px",
                        margin="0 auto",
                        max_width="720px",
                        padding="40px 20px 40px 20px",
                        font_family=basic_font,
                    ),
                    *content
                ),
                tags.Text(table_ie9_close),
            ),
        )
        res = html.render()
        if display:
            IPython.core.display.display(IPython.core.display.HTML(res))
        return res