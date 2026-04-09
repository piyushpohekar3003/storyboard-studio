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
)
from services.exporter import markdown_to_docx, script_to_docx

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
