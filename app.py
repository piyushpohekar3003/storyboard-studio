import json
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit

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
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()


# --- Routes ---


@app.route("/")
def index():
    return render_template("index.html", channels=list_channels())


@app.route("/dataviz")
def dataviz():
    return render_template("dataviz.html")


@app.route("/create", methods=["POST"])
def create():
    topic = request.form.get("topic", "Untitled")
    channels_json = request.form.get("channels", "[]")
    selected_channels = json.loads(channels_json)
    research_text = request.form.get("research_text", "")
    source_url = request.form.get("source_url", "")

    research_images_json = None

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

    # Redirect to first project
    return jsonify({"redirect": f"/generate/{project_ids[0]}", "project_ids": project_ids})


@app.route("/generate/<int:project_id>")
def generate(project_id):
    project = get_project(project_id)
    if not project:
        return "Project not found", 404

    channel = get_channel(project["channel_slug"])
    channel_name = channel["name"] if channel else project["channel_slug"]

    # Find sibling projects (same topic, different channels)
    all_projects = list_projects()
    siblings = [
        {"id": p["id"], "channel_name": get_channel(p["channel_slug"])["name"]}
        for p in all_projects
        if p["topic"] == project["topic"] and p["id"] != project["id"]
    ]
    if siblings:
        siblings.insert(
            0, {"id": project["id"], "channel_name": channel_name}
        )

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


# --- SocketIO Events ---


@socketio.on("generate_script")
def handle_generate_script(data):
    project_id = data["project_id"]
    channel_slug = data["channel"]
    project = get_project(project_id)
    channel = get_channel(channel_slug)

    if not project or not channel:
        emit("error", {"message": "Project or channel not found"})
        return

    try:
        # Parse stored images
        images = json.loads(project["research_images"]) if project.get("research_images") else []

        full_text = ""
        for chunk in generate_script_stream(project["research_input"], channel, images):
            full_text += chunk
            emit("script_chunk", {"project_id": project_id, "text": chunk})

        update_project(project_id, generated_script=full_text, status="script_done")
        emit("script_done", {"project_id": project_id})
    except Exception as e:
        emit("error", {"message": str(e)})


@socketio.on("generate_storyboard")
def handle_generate_storyboard(data):
    project_id = data["project_id"]
    channel_slug = data["channel"]
    script_text = data.get("script_text", "")
    channel = get_channel(channel_slug)

    if not channel:
        emit("error", {"message": "Channel not found"})
        return

    # Save edited script if different
    project = get_project(project_id)
    if script_text and script_text != project.get("generated_script"):
        update_project(project_id, edited_script=script_text)

    try:
        full_text = ""
        for chunk in generate_storyboard_stream(script_text, channel):
            full_text += chunk
            emit("storyboard_chunk", {"project_id": project_id, "text": chunk})

        update_project(project_id, generated_storyboard=full_text, status="complete")
        emit("storyboard_done", {"project_id": project_id})
    except Exception as e:
        emit("error", {"message": str(e)})


@socketio.on("redo_script")
def handle_redo_script(data):
    project_id = data["project_id"]
    channel_slug = data["channel"]
    mode = data.get("mode", "full")
    feedback = data.get("feedback", "")
    selected_text = data.get("selected_text", "")
    channel = get_channel(channel_slug)
    project = get_project(project_id)

    if not channel or not project:
        emit("error", {"message": "Project or channel not found"})
        return

    current_script = project.get("edited_script") or project.get("generated_script", "")

    try:
        full_text = ""
        if mode == "section" and selected_text:
            stream = redo_section_stream(current_script, selected_text, feedback, channel, "script")
        else:
            stream = redo_full_stream(current_script, feedback, channel, "script")

        for chunk in stream:
            full_text += chunk
            emit("redo_script_chunk", {"project_id": project_id, "text": chunk})

        update_project(project_id, edited_script=full_text)
        emit("redo_script_done", {"project_id": project_id})
    except Exception as e:
        emit("error", {"message": str(e)})


@socketio.on("redo_storyboard")
def handle_redo_storyboard(data):
    project_id = data["project_id"]
    channel_slug = data["channel"]
    feedback = data.get("feedback", "")
    channel = get_channel(channel_slug)
    project = get_project(project_id)

    if not channel or not project:
        emit("error", {"message": "Project or channel not found"})
        return

    current_storyboard = project.get("generated_storyboard", "")

    try:
        full_text = ""
        stream = redo_full_stream(current_storyboard, feedback, channel, "storyboard")
        for chunk in stream:
            full_text += chunk
            emit("redo_storyboard_chunk", {"project_id": project_id, "text": chunk})

        update_project(project_id, generated_storyboard=full_text)
        emit("redo_storyboard_done", {"project_id": project_id})
    except Exception as e:
        emit("error", {"message": str(e)})


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
