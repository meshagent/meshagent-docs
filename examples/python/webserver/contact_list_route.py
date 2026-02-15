from __future__ import annotations

from html import escape

from aiohttp import web

from meshagent.api.room_server_client import TextDataType

METHODS = ["GET"]

_PAGE_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Contact list</title>
    <style>
      :root {{
        color-scheme: light;
        --ink: #1d1f24;
        --muted: #58606b;
        --surface: #ffffff;
        --accent: #0f766e;
        --accent-2: #0b5d56;
        --border: #d8dde6;
        --shadow: 0 18px 40px rgba(26, 31, 41, 0.12);
        --radius: 18px;
        --font: "Instrument Sans", "Space Grotesk", "Segoe UI", sans-serif;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: var(--font);
        color: var(--ink);
        background:
          radial-gradient(1200px 600px at 0% 0%, #e0f2f1 0%, transparent 60%),
          radial-gradient(900px 500px at 100% 0%, #e8f0ff 0%, transparent 60%),
          #f6f7fb;
        min-height: 100vh;
        display: grid;
        place-items: center;
        padding: 32px 20px;
      }}
      .card {{
        width: min(760px, 100%);
        background: var(--surface);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        border: 1px solid #eef1f6;
        padding: 28px 28px 24px;
      }}
      header {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 22px;
      }}
      h1 {{
        font-size: clamp(26px, 4vw, 34px);
        margin: 0;
        letter-spacing: -0.02em;
      }}
      p {{
        margin: 0;
        color: var(--muted);
        line-height: 1.5;
      }}
      .meta {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
      }}
      .badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--accent-2);
        background: rgba(15, 118, 110, 0.12);
      }}
      .items {{
        display: grid;
        gap: 16px;
      }}
      .item {{
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 16px 18px;
        background: #fcfdff;
      }}
      .item h2 {{
        margin: 0;
        font-size: 1.1rem;
      }}
      .item span {{
        color: var(--muted);
        font-size: 0.95rem;
      }}
      .item p {{
        margin: 10px 0 0;
        color: var(--ink);
      }}
      .empty {{
        padding: 18px;
        border-radius: 14px;
        border: 1px dashed var(--border);
        color: var(--muted);
        background: #fafbff;
      }}
      @media (max-width: 520px) {{
        .card {{ padding: 22px; }}
      }}
    </style>
  </head>
  <body>
    <main class="card">
      <header>
        <h1>Saved contacts</h1>
        <div class="meta">
          <p>Recent form submissions stored in the MeshAgent room database.</p>
          <span class="badge">{total_count} total</span>
        </div>
      </header>
      {list_html}
    </main>
  </body>
</html>
"""


def _render_contacts(contacts: list[dict]) -> str:
    if not contacts:
        return (
            '<p class="empty">No contacts yet. Submit the contact form to add one.</p>'
        )

    items: list[str] = []
    for contact in contacts:
        name = escape(str(contact.get("name", "")).strip()) or "Unknown"
        email = escape(str(contact.get("email", "")).strip()) or "Not provided"
        message = (
            escape(str(contact.get("message", "")).strip()) or "No message provided."
        )
        items.append(
            """<article class="item">
  <div class="meta">
    <h2>{name}</h2>
    <span>{email}</span>
  </div>
  <p>{message}</p>
</article>""".format(
                name=name,
                email=email,
                message=message,
            )
        )

    return '<section class="items">{items}</section>'.format(items="\n".join(items))


async def handler(*, room, req: web.Request) -> web.StreamResponse:
    if req.method != "GET":
        return web.Response(status=405)

    await room.database.create_table_with_schema(
        name="contacts",
        schema={
            "name": TextDataType(),
            "email": TextDataType(),
            "message": TextDataType(),
        },
        mode="create_if_not_exists",
        data=None,
    )
    contacts = await room.database.search(table="contacts")
    html = _PAGE_HTML.format(
        total_count=len(contacts),
        list_html=_render_contacts(contacts),
    )
    return web.Response(text=html, content_type="text/html")
