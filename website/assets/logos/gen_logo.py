from PIL import Image, ImageDraw, ImageFont

S = 512
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# dark rounded badge
d.rounded_rectangle([0, 0, S, S], radius=120, fill=(10, 14, 26, 255))

# gold border
border = Image.new("RGBA", (S, S), (0, 0, 0, 0))
db = ImageDraw.Draw(border)
db.rounded_rectangle([28, 28, S - 28, S - 28], radius=96, outline=(245, 166, 35, 217), width=6)
img = Image.alpha_composite(img, border)
d = ImageDraw.Draw(img)

# font (Microsoft YaHei Bold, fallback SimHei)
gold = (245, 166, 35, 255)
try:
    f = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 156, index=0)
except Exception:
    try:
        f = ImageFont.truetype(r"C:\Windows\Fonts\simhei.ttf", 156)
    except Exception:
        f = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 156, index=1)

d.text((256, 206), "惠", font=f, fill=gold, anchor="mm")
d.text((256, 356), "帮", font=f, fill=gold, anchor="mm")

out = r"E:\Jack_Fulfillment_Business\01_代发货履约\website\assets\logos\logoB_monogram.png"
img.save(out)
print("saved", out)
