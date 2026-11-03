"""Render maintained bilingual documentation diagrams. Requires Pillow >= 10.

Usage: python docs/render_diagrams.py [--font PATH] [--bold-font PATH]
The JSON source controls every public label, node, edge and palette color.
The renderer never calls a model, reads credentials, or executes the skill.
"""
import argparse, hashlib, json, math, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent

def choose_font(value,bold=False):
    if value:
        p=Path(value)
        if not p.is_file(): raise FileNotFoundError(p)
        return p
    candidates=[Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'/('msyhbd.ttc' if bold else 'msyh.ttc'),Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')]
    for p in candidates:
        if p.is_file(): return p
    raise RuntimeError('Provide a CJK-capable font using --font and --bold-font.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--font');p.add_argument('--bold-font');p.add_argument('--output',type=Path,default=HERE/'assets');args=p.parse_args()
    fontfile=choose_font(args.font); boldfile=choose_font(args.bold_font,True)
    spec=json.loads((HERE/'diagram-source.json').read_text(encoding='utf-8'))
    pal=spec['palette']; args.output.mkdir(parents=True,exist_ok=True); results=[]
    for name,diagram in spec['diagrams'].items():
        for lang in ('zh','en'):
            im=Image.new('RGB',tuple(diagram['size']),pal['paper']);d=ImageDraw.Draw(im)
            fonts={n:ImageFont.truetype(str(boldfile if n in ('heading','title') else fontfile),size) for n,size in [('heading',54),('subtitle',31),('title',37),('body',29),('small',26),('index',28)]}
            overflow=[]
            def measure(s,font): return d.textlength(s,font=font)
            def wrap(s,font,width):
                if measure(s,font)<=width:return [s]
                tokens=s.split(' ') if lang=='en' else list(s); out=[];line='';sep=' ' if lang=='en' else ''
                for token in tokens:
                    candidate=line+sep+token if line else token
                    if line and measure(candidate,font)>width:out.append(line);line=token
                    else:line=candidate
                if line:out.append(line)
                return out
            def text_lines(lines,x,y,font,width,fill,gap=10):
                all_lines=[line for s in lines for line in wrap(s,font,width)]
                for line in all_lines:
                    d.text((x,y),line,font=font,fill=fill,anchor='lt');y+=font.size+gap
                return y,all_lines
            d.rounded_rectangle((60,55,145,67),radius=6,fill=pal['coral'])
            y,_=text_lines([diagram['title'][lang]],60,95,fonts['heading'],diagram['size'][0]-120,pal['ink'],8)
            # English workflow title is deliberately one line at the chosen width.
            if y>170: overflow.append('heading_too_tall')
            d.text((62,166),diagram['subtitle'][lang],font=fonts['subtitle'],fill=pal['muted'],anchor='lt')
            def arrowhead(end,previous,color):
                ang=math.atan2(end[1]-previous[1],end[0]-previous[0]);length=15;wing=8
                points=[end,(end[0]-length*math.cos(ang)+wing*math.sin(ang),end[1]-length*math.sin(ang)-wing*math.cos(ang)),(end[0]-length*math.cos(ang)-wing*math.sin(ang),end[1]-length*math.sin(ang)+wing*math.cos(ang))]
                d.polygon(points,fill=color)
            for edge in diagram['edges']:
                pts=[tuple(v) for v in edge['points']]; color=pal.get(edge.get('color',''),pal['ink'])
                if edge.get('dashed'):
                    for a,b in zip(pts,pts[1:]):
                        length=math.dist(a,b)
                        for start in range(0,int(length),22):
                            stop=min(start+12,length);d.line((a[0]+(b[0]-a[0])*start/length,a[1]+(b[1]-a[1])*start/length,a[0]+(b[0]-a[0])*stop/length,a[1]+(b[1]-a[1])*stop/length),fill=color,width=4)
                else:d.line(pts,fill=color,width=4,joint='curve')
                arrowhead(pts[-1],pts[-2],color)
                if edge.get('both'):arrowhead(pts[0],pts[1],color)
                if edge.get('label'):
                    tx,ty=edge['label_at'];label=edge['label'][lang];f=fonts['small'];w=measure(label,f)
                    d.rounded_rectangle((tx-w/2-7,ty-5,tx+w/2+7,ty+f.size+5),radius=6,fill=pal['paper']);d.text((tx,ty),label,font=f,fill=pal['muted'],anchor='mt')
            nodes=[]
            for node in diagram['nodes']:
                x,y,w,h=node['box'];accent=pal[node['color']];branch=node.get('branch',False)
                fill=pal['blue_light'] if branch and node['color']=='blue' else pal['coral_light'] if branch and node['color']=='coral' else pal['yellow'] if branch else pal['white']
                d.rounded_rectangle((x,y,x+w,y+h),radius=21,fill=fill,outline=pal['line'],width=1)
                d.rounded_rectangle((x,y,x+9,y+h),radius=4,fill=accent)
                left=x+28
                if node.get('index'):
                    d.ellipse((x+26,y+25,x+79,y+78),fill=accent)
                    index_color=pal['ink'] if node['color']=='yellow' else pal['white']
                    d.text((x+52.5,y+51.5),node['index'],font=fonts['index'],fill=index_color,anchor='mm')
                    left=x+99
                width=x+w-25-left
                end,titlelines=text_lines([node['title'][lang]],left,y+26,fonts['title'],width,pal['ink'],8)
                end+=12
                end,bodylines=text_lines(node['body'][lang],left,end,fonts['body'],width,pal['muted'],12)
                if end-12>y+h-12:overflow.append({'node':node['id'],'bottom':end-12,'allowed':y+h-12,'lines':titlelines+bodylines})
                nodes.append({'id':node['id'],'title':titlelines,'body':bodylines,'text_bottom':end,'box_bottom':y+h})
            yy=diagram['size'][1]-80
            _,note=text_lines([diagram['note'][lang]],70,yy,fonts['small'],diagram['size'][0]-140,pal['muted'],8)
            path=args.output/f'{name}-{lang}.png';im.save(path,optimize=True)
            with Image.open(path) as check:check.load();size=list(check.size)
            results.append({'file':path.name,'size':size,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'text_overflow':overflow,'nodes':nodes,'note':note})
    print(json.dumps({'source':'diagram-source.json','files':results},ensure_ascii=False,indent=2))
    if any(r['text_overflow'] for r in results):raise SystemExit('Diagram text overflow: inspect render output')

if __name__=='__main__': main()
