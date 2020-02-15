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
    "斗破苍穹": {},
    "三眼啸天录":{},
    "萌三国":{}
}


@app.route("/mh/<string:mh_name>")
def mh_toc(mh_name):
    if mh_name in mh:
        if "sections" not in mh[mh_name]:
            do_mh_update(mh_name)
        sections=mh[mh_name]["sections"]
        return render_template("mh_toc.html", title=mh_name, mh_name=mh_name,sections=sections)
    else:
        return "未找到",404

@app.route("/mh/<string:mh_name>/<int:mh_section>")
def mh_content(mh_name, mh_section):
    if "sections" not in mh[mh_name]:
        do_mh_update(mh_name)

    sections=mh[mh_name]["sections"]
    for i,section in enumerate(sections):
        if int(section["iid"]) == mh_section:
            break
    if i>=len(sections)-1:
        nxt_section= {
                "iid": "0", 
                "name": f"已读完?点击更新章节", 
                "url": f"/mh/update/{mh_name}", 
                # "img_urls":[img_ptn.format(img_id=img_id) for img_id in range(chapter["start_num"],chapter["end_num"]+1)]
                }
    else:
        nxt_section=sections[i+1]
    return render_template("mh_section.html",mh_name=mh_name,section_name=section["name"],nxt_url=nxt_section['url'],nxt_name=f"下一章: {nxt_section['name']}",section_id=mh_section,**section)

# def mh_update()


def do_mh_update(mh_name):
    kai_id={
        "斗破苍穹":"25934",
        "三眼啸天录":"8458",
        "萌三国":"8255",
        }
    if mh_name in kai_id:
        src_url=f"https://www.kaimanhua.com/api/getComicInfoBody?product_id=14&productname=kaimh&platformname=pc&comic_id={kai_id[mh_name]}"
        req= requests.get(src_url)
        # with open("db/dpcq_src.json","wb") as fp:
        #     fp.write(req.content)
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
                "url": f"/mh/{mh_name}/{i}", 
                "img_urls":[img_ptn.format(img_id=img_id) for img_id in range(chapter["start_num"],chapter["end_num"]+1)]
                }
            sections.append(new_section)

        mh[mh_name]["sections"]=sections
        #  = [
        #                         for i in range(1, 826)]

@app.route("/mh/update/<string:mh_name>")
def mh_update(mh_name):
    do_mh_update(mh_name)
    return "ok"

# if __name__ == "__main__":
#     do_mh_update("斗破苍穹")