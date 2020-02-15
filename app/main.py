from flask import Flask, request, render_template
import json

app = Flask(
    "lei_garden",
    template_folder="template"
)


@app.route("/")
def index():
    return render_template("index.html")


mh = {
    "斗破苍穹": {}
}
with open("db/dpcq.json") as fp:

    dpcq_img_count = json.load(fp)
mh["斗破苍穹"]["sections"] = [{"iid": f"{i}", "name": f"第{i}章", "url": f"/mh/斗破苍穹/{i}", "img_count": dpcq_img_count.get(str(i),0)}
                          for i in range(1, 826)]


@app.route("/mh/<string:mh_name>")
def mh_toc(mh_name):
    if mh_name == "斗破苍穹":
        sections=mh[mh_name]["sections"]
        return render_template("mh_toc.html", title="斗破苍穹", sections=sections)


@app.route("/mh/<string:mh_name>/<int:mh_section>")
def mh_content(mh_name, mh_section):
    sections=mh[mh_name]["sections"]
    for section in sections:
        if int(section["iid"]) == mh_section:
            break
    return render_template("mh_section.html",mh_name=mh_name,section_name=section["name"],nxt_url=f"/mh/{mh_name}/{mh_section+1}",nxt_name=f"下一章：第{mh_section+1}章",section_id=mh_section,img_count=section["img_count"])
