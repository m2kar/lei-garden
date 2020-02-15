from flask import Flask, request, render_template
import json
import requests

app = Flask(
    "lei_garden",
    template_folder="template"
)


@app.route("/")
def index():
    do_mh_update("斗破苍穹")
    return render_template("index.html")


mh = {
    "斗破苍穹": {}
}


@app.route("/mh/<string:mh_name>")
def mh_toc(mh_name):
    if mh_name == "斗破苍穹":
        if "sections" not in mh[mh_name]:
            do_mh_update(mh_name)
        sections=mh[mh_name]["sections"]
        return render_template("mh_toc.html", title="斗破苍穹", sections=sections)


@app.route("/mh/<string:mh_name>/<int:mh_section>")
def mh_content(mh_name, mh_section):
    if "sections" not in mh[mh_name]:
        do_mh_update(mh_name)

    sections=mh[mh_name]["sections"]
    for section in sections:
        if int(section["iid"]) == mh_section:
            break
    return render_template("mh_section.html",mh_name=mh_name,section_name=section["name"],nxt_url=f"/mh/{mh_name}/{mh_section+1}",nxt_name=f"下一章：第{mh_section+1}章",section_id=mh_section,**section)

# def mh_update()


def do_mh_update(mh_name):
    if mh_name=="斗破苍穹":
        dpcq_src_url="https://www.kaimanhua.com/api/getComicInfoBody?product_id=14&productname=kaimh&platformname=pc&comic_id=25934"
        req= requests.get(dpcq_src_url)
        with open("db/dpcq_src.json","wb") as fp:
            fp.write(req.content)
        # mh["斗破苍穹"]

        # with open("db/dpcq_src.json") as fp:
        #     dpcq_src=json.load(fp)
        #     # dpcq_img_count = json.load(fp)
        dpcq_src=req.json()
        sections=[]
        for _i, chapter in enumerate(dpcq_src["data"]["comic_chapter"][::-1]):
            # i=int(chapter["chapter_id"])
            i=_i+1
            img_ptn=f"https://mhpic.{chapter['chapter_domain']}{chapter['rule']}-kaimh.high.webp".replace("$$","{img_id}")
            new_section={
                "iid": f"{i}", 
                "name": f"{chapter['chapter_name']}", 
                "url": f"/mh/斗破苍穹/{i}", 
                "img_urls":[img_ptn.format(img_id=img_id) for img_id in range(chapter["start_num"],chapter["end_num"]+1)]
                }
            sections.append(new_section)

        mh["斗破苍穹"]["sections"]=sections
        #  = [
        #                         for i in range(1, 826)]

@app.route("/mh/update/<string:mh_name>")
def mh_update(mh_name):
    do_mh_update(mh_name)
    return "ok"

if __name__ == "__main__":
    do_mh_update("斗破苍穹")