import json
import os
import zipfile
import subprocess
import tempfile
from flask import Flask, render_template, request, jsonify, send_file, Response, stream_with_context

from config import DB_PATH
from database import init_db, save_project, update_project, get_project, list_projects
from channels import get_channel, list_channels
from services.doc_fetcher import fetch_google_doc, is_google_doc_url
from services.generator import (
    generate_script_stream,
    generate_storyboard_stream,
    redo_section_stream,
    redo_full_stream,
    structure_script_stream,
    generate_visuals_stream,
)
from services.exporter import markdown_to_docx, script_to_docx, bytes_visuals_to_docx, bytes_visuals_to_pdf
from services.image_extractor import extract_from_file, save_images_to_disk
from services.shorts_storyboard import (
    generate_visual_storyboard_stream,
    add_image_to_storyboard_stream,
    parse_storyboard_json,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "storyboard-generator-secret"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

init_db()


# --- Helpers ---

def sse_stream(generator):
    """Wrap a text generator as an SSE response."""
    def generate():
        full_text = ""
        for chunk in generator:
            full_text += chunk
            yield f"data: {json.dumps({'text': chunk})}\n\n"
        yield f"data: {json.dumps({'done': True, 'full_text': full_text})}\n\n"
    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


def extract_text_from_file(file):
    """Extract text from uploaded file (.txt, .docx, .pdf)."""
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")

    elif filename.endswith(".docx"):
        # DOCX is a zip of XML files
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        try:
            with zipfile.ZipFile(tmp_path, "r") as z:
                if "word/document.xml" in z.namelist():
                    import re
                    xml = z.read("word/document.xml").decode("utf-8")
                    # Strip XML tags, keep text
                    text = re.sub(r"<[^>]+>", " ", xml)
                    text = re.sub(r"\s+", " ", text).strip()
                    return text
            return ""
        finally:
            os.unlink(tmp_path)

    elif filename.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        try:
            result = subprocess.run(
                ["pdftotext", tmp_path, "-"],
                capture_output=True, text=True, timeout=30,
            )
            return result.stdout if result.returncode == 0 else ""
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return ""
        finally:
            os.unlink(tmp_path)

    elif filename.endswith(".doc"):
        return file.read().decode("utf-8", errors="ignore")

    return ""


# --- Routes ---

@app.route("/")
def index():
    return render_template("index.html", channels=list_channels())


@app.route("/create", methods=["POST"])
def create():
    topic = request.form.get("topic", "").strip() or "Untitled"
    channels_json = request.form.get("channels", "[]")
    selected_channels = json.loads(channels_json)
    research_text = request.form.get("research_text", "")
    source_url = request.form.get("source_url", "")
    research_images_json = None

    # Handle file upload
    if "research_file" in request.files:
        file = request.files["research_file"]
        if file and file.filename:
            research_text = extract_text_from_file(file)

    # Fetch from Google Doc if URL provided
    if source_url and is_google_doc_url(source_url):
        try:
            research_text, images = fetch_google_doc(source_url)
            if images:
                research_images_json = json.dumps(images)
        except Exception as e:
            return jsonify({"error": f"Failed to fetch doc: {str(e)}"}), 400

    if not research_text:
        return jsonify({"error": "No research content provided"}), 400

    # Create a project for each selected channel
    project_ids = []
    for ch_slug in selected_channels:
        pid = save_project(ch_slug, topic, research_text, source_url or None, research_images_json)
        project_ids.append(pid)

    return jsonify({"redirect": f"/generate/{project_ids[0]}", "project_ids": project_ids})


@app.route("/generate/<int:project_id>")
def generate(project_id):
    project = get_project(project_id)
    if not project:
        return "Project not found", 404

    channel = get_channel(project["channel_slug"])
    channel_name = channel["name"] if channel else project["channel_slug"]

    all_projects = list_projects()
    siblings = [
        {"id": p["id"], "channel_name": get_channel(p["channel_slug"])["name"]}
        for p in all_projects
        if p["topic"] == project["topic"] and p["id"] != project["id"]
    ]
    if siblings:
        siblings.insert(0, {"id": project["id"], "channel_name": channel_name})

    return render_template(
        "generate.html",
        project=project,
        channel_name=channel_name,
        sibling_ids=siblings if siblings else None,
    )


@app.route("/bytes")
def bytes_page():
    return render_template("bytes.html")


@app.route("/api/bytes/structure", methods=["POST"])
def bytes_structure():
    from config import ANTHROPIC_API_KEY
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    script = request.form.get("script", "")
    category = request.form.get("category", "")
    if not script or not category:
        return jsonify({"error": "Script and category required"}), 400

    return sse_stream(structure_script_stream(script, category))


@app.route("/api/bytes/visuals", methods=["POST"])
def bytes_visuals():
    from config import ANTHROPIC_API_KEY
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    script = request.form.get("script", "")
    category = request.form.get("category", "")
    if not script or not category:
        return jsonify({"error": "Script and category required"}), 400

    return sse_stream(generate_visuals_stream(script, category))


@app.route("/api/bytes/export", methods=["POST"])
def bytes_export():
    visuals_raw = request.form.get("visuals", "[]")
    script_text = request.form.get("script", "")
    title = request.form.get("title", "A1 Bytes — Visual Storyboard")

    try:
        visuals = json.loads(visuals_raw)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid visuals JSON"}), 400

    buffer = bytes_visuals_to_pdf(visuals, script_text, title)
    safe_title = title[:50].replace("/", "-")
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{safe_title}.pdf",
        mimetype="application/pdf",
    )


@app.route("/history")
def history():
    channel_filter = request.args.get("channel")
    projects = list_projects(channel_filter)
    return render_template(
        "history.html",
        projects=projects,
        channels=list_channels(),
        filter=channel_filter,
    )


# --- SSE Streaming Endpoints ---

@app.route("/api/stream-script/<int:project_id>")
def stream_script(project_id):
    from config import ANTHROPIC_API_KEY
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    project = get_project(project_id)
    channel = get_channel(project["channel_slug"]) if project else None
    if not project or not channel:
        return jsonify({"error": "Not found"}), 404

    try:
        images = json.loads(project["research_images"]) if project.get("research_images") else []
        return sse_stream(generate_script_stream(project["research_input"], channel, images))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stream-storyboard/<int:project_id>", methods=["POST"])
def stream_storyboard(project_id):
    project = get_project(project_id)
    channel = get_channel(project["channel_slug"]) if project else None
    if not project or not channel:
        return jsonify({"error": "Not found"}), 404

    script_text = request.form.get("script_text", "")
    if script_text and script_text != project.get("generated_script"):
        update_project(project_id, edited_script=script_text)

    return sse_stream(generate_storyboard_stream(script_text, channel))


@app.route("/api/redo/<int:project_id>", methods=["POST"])
def redo(project_id):
    project = get_project(project_id)
    channel = get_channel(project["channel_slug"]) if project else None
    if not project or not channel:
        return jsonify({"error": "Not found"}), 404

    content_type = request.form.get("type", "script")
    mode = request.form.get("mode", "full")
    feedback = request.form.get("feedback", "")
    selected_text = request.form.get("selected_text", "")

    if content_type == "script":
        current = project.get("edited_script") or project.get("generated_script", "")
    else:
        current = project.get("generated_storyboard", "")

    if mode == "section" and selected_text:
        gen = redo_section_stream(current, selected_text, feedback, channel, content_type)
    else:
        gen = redo_full_stream(current, feedback, channel, content_type)

    return sse_stream(gen)


@app.route("/api/save", methods=["POST"])
def save():
    """Save generated content after streaming completes."""
    project_id = int(request.form.get("project_id", 0))
    content_type = request.form.get("type", "script")
    content = request.form.get("content", "")

    if content_type == "script":
        update_project(project_id, generated_script=content, status="script_done")
    elif content_type == "storyboard":
        update_project(project_id, generated_storyboard=content, status="complete")
    elif content_type == "redo_script":
        update_project(project_id, edited_script=content)
    elif content_type == "redo_storyboard":
        update_project(project_id, generated_storyboard=content)

    return jsonify({"ok": True})


# --- Export ---

@app.route("/export/<int:project_id>")
def export(project_id):
    project = get_project(project_id)
    if not project or not project["generated_storyboard"]:
        return "No storyboard to export", 404

    buffer = markdown_to_docx(project["generated_storyboard"], title=project["topic"])
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{project['topic'][:50]} - Storyboard.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@app.route("/export-script/<int:project_id>")
def export_script(project_id):
    project = get_project(project_id)
    script = project.get("edited_script") or project.get("generated_script") if project else None
    if not script:
        return "No script to export", 404

    buffer = script_to_docx(script, title=project["topic"])
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{project['topic'][:50]} - Script.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


# --- Shorts Visual Storyboard ---


@app.route("/shorts")
def shorts_page():
    return render_template("shorts.html")


@app.route("/api/shorts/upload", methods=["POST"])
def shorts_upload():
    """Extract text + images from an uploaded file."""
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    with tempfile.NamedTemporaryFile(
        suffix=os.path.splitext(file.filename)[1], delete=False
    ) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        text, images = extract_from_file(tmp_path)
        # Strip base64 data from response to keep it small — store separately
        image_summaries = [
            {"index": i, "description": img.get("description", f"Image {i}"),
             "width": img.get("width", 0), "height": img.get("height", 0)}
            for i, img in enumerate(images)
        ]
        # Save images to a temp project dir
        import time
        project_dir = f"projects/{int(time.time() * 1000)}"
        os.makedirs(f"static/{project_dir}/screenshots", exist_ok=True)
        save_images_to_disk(images, f"static/{project_dir}/screenshots")

        # Store images in session-like temp storage (as JSON file)
        with open(f"static/{project_dir}/images.json", "w") as f:
            json.dump(images, f)

        return jsonify({
            "text": text,
            "images": image_summaries,
            "project_dir": project_dir,
            "image_count": len(images),
        })
    finally:
        os.unlink(tmp_path)


@app.route("/api/shorts/fetch-gdoc", methods=["POST"])
def shorts_fetch_gdoc():
    """Extract text + images from a Google Doc URL."""
    url = request.form.get("url", "")
    if not is_google_doc_url(url):
        return jsonify({"error": "Invalid Google Doc URL"}), 400

    text, images = extract_from_file(url)

    import time
    project_dir = f"projects/{int(time.time() * 1000)}"
    os.makedirs(f"static/{project_dir}/screenshots", exist_ok=True)
    save_images_to_disk(images, f"static/{project_dir}/screenshots")

    with open(f"static/{project_dir}/images.json", "w") as f:
        json.dump(images, f)

    image_summaries = [
        {"index": i, "description": img.get("description", f"Image {i}"),
         "width": img.get("width", 0), "height": img.get("height", 0)}
        for i, img in enumerate(images)
    ]

    return jsonify({
        "text": text,
        "images": image_summaries,
        "project_dir": project_dir,
        "image_count": len(images),
    })


@app.route("/api/shorts/generate", methods=["POST"])
def shorts_generate():
    """SSE stream — LLM generates visual storyboard JSON."""
    script = request.form.get("script", "")
    project_dir = request.form.get("project_dir", "")

    # Create project dir if not set (user pasted text without uploading)
    if not project_dir:
        import time
        project_dir = f"projects/{int(time.time() * 1000)}"
        os.makedirs(f"static/{project_dir}/screenshots", exist_ok=True)

    # Load images from the project dir
    images = []
    images_path = f"static/{project_dir}/images.json"
    if os.path.exists(images_path):
        with open(images_path, "r") as f:
            images = json.load(f)

    return sse_stream(generate_visual_storyboard_stream(script, images))


@app.route("/api/shorts/render", methods=["POST"])
def shorts_render():
    """Takes JSON, generates SVG files + storyboard HTML, returns paths."""
    import shutil

    storyboard_json = request.get_json()
    if not storyboard_json:
        return jsonify({"error": "No storyboard JSON provided"}), 400

    project_dir = storyboard_json.get("_project_dir", "")
    if not project_dir:
        import time
        project_dir = f"projects/{int(time.time() * 1000)}"
        os.makedirs(f"static/{project_dir}", exist_ok=True)

    # Lazy import to avoid circular dependency at startup
    from services.svg_generator import ShortsFrameRenderer, generate_storyboard_html

    renderer = ShortsFrameRenderer()
    svg_paths = []
    frame_num = 0

    for section in storyboard_json.get("sections", []):
        for frame in section.get("frames", []):
            frame_num += 1
            svg_string = renderer.render(
                frame,
                screenshot_dir=f"screenshots",
                aparna_path="aparna.png",
            )
            filename = f"frame-{frame_num:02d}.svg"
            filepath = f"static/{project_dir}/{filename}"
            with open(filepath, "w") as f:
                f.write(svg_string)
            svg_paths.append(f"/static/{project_dir}/{filename}")

    # Copy aparna.png into project dir
    aparna_src = os.path.join("static", "aparna.png")
    aparna_dst = os.path.join("static", project_dir, "aparna.png")
    if os.path.exists(aparna_src) and not os.path.exists(aparna_dst):
        shutil.copy2(aparna_src, aparna_dst)

    # Generate storyboard HTML
    html_content = generate_storyboard_html(storyboard_json, project_dir)
    html_path = f"static/{project_dir}/storyboard.html"
    with open(html_path, "w") as f:
        f.write(html_content)

    return jsonify({
        "project_dir": project_dir,
        "svg_paths": svg_paths,
        "html_path": f"/{html_path}",
        "total_frames": frame_num,
    })


@app.route("/api/shorts/export-pdf", methods=["POST"])
def shorts_export_pdf():
    """Generate PDF and return as download."""
    storyboard_json = request.get_json()
    if not storyboard_json:
        return jsonify({"error": "No storyboard JSON"}), 400

    project_dir = storyboard_json.get("_project_dir", "")
    title = storyboard_json.get("metadata", {}).get("title", "Shorts Storyboard")

    from services.exporter import shorts_storyboard_to_pdf
    buffer = shorts_storyboard_to_pdf(storyboard_json, f"static/{project_dir}", title)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{title[:50]}.pdf",
        mimetype="application/pdf",
    )


@app.route("/api/shorts/redo", methods=["POST"])
def shorts_redo():
    """SSE stream — regenerate with feedback."""
    script = request.form.get("script", "")
    feedback = request.form.get("feedback", "")
    previous_json = request.form.get("storyboard_json", "")
    project_dir = request.form.get("project_dir", "")

    images = []
    images_path = f"static/{project_dir}/images.json"
    if os.path.exists(images_path):
        with open(images_path, "r") as f:
            images = json.load(f)

    return sse_stream(
        generate_visual_storyboard_stream(script, images, feedback=feedback, previous_json=previous_json)
    )


@app.route("/api/shorts/add-image", methods=["POST"])
def shorts_add_image():
    """Add a new image and get LLM to place it in the storyboard."""
    file = request.files.get("file")
    script = request.form.get("script", "")
    storyboard_json = request.form.get("storyboard_json", "")
    project_dir = request.form.get("project_dir", "")

    if not file:
        return jsonify({"error": "No file"}), 400

    import base64
    from PIL import Image as PILImage
    import io

    img_bytes = file.read()
    b64 = base64.b64encode(img_bytes).decode()
    content_type = file.content_type or "image/png"

    # Get dimensions
    try:
        pil_img = PILImage.open(io.BytesIO(img_bytes))
        w, h = pil_img.size
    except Exception:
        w, h = 0, 0

    new_image = {
        "media_type": content_type,
        "data": b64,
        "description": f"User-uploaded image ({w}x{h}px)",
        "width": w,
        "height": h,
    }

    # Save to screenshots dir
    screenshots_dir = f"static/{project_dir}/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    existing = len([f for f in os.listdir(screenshots_dir) if f.startswith("img_")])
    new_path = os.path.join(screenshots_dir, f"img_{existing}.png")
    with open(new_path, "wb") as f:
        f.write(img_bytes)

    # Also update images.json
    images_path = f"static/{project_dir}/images.json"
    images = []
    if os.path.exists(images_path):
        with open(images_path, "r") as f:
            images = json.load(f)
    images.append(new_image)
    with open(images_path, "w") as f:
        json.dump(images, f)

    return sse_stream(add_image_to_storyboard_stream(storyboard_json, new_image, script))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
