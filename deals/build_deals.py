
import urllib.request, json, datetime, time, re, os
os.makedirs("/home/user/site", exist_ok=True)
POSTAL="17603"
def get(url):
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36","Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=45) as r: return r.read()

RULES=[
 ("Baby",["diaper","formula","baby wipe","pampers","huggies","enfamil","similac","onesie"]),
 ("Pet",["dog food","cat food","puppy","kitten"," pet ","purina","friskies","meow mix","pedigree","milk-bone","cat litter","dog treat","dog ","cat "]),
 ("Produce",["lettuce","tomato","potato","onion","apple","banana","grape","blueberr","strawberr","raspberr","blackberr","melon","avocado","broccoli","spinach","salad","carrot","celery","cucumber","lemon","lime","orange","peach","plum","pear","mango","pineapple"," corn","mushroom","squash","zucchini","cabbage","kale","produce","fresh fruit","vegetable","cilantro","garlic","cherr","clementine","grapefruit","asparagus","berries","berry"]),
 ("Meat & Seafood",["beef","steak","chicken","pork","turkey","bacon","sausage"," ham","ground ","loin","ribs","chops","frank","hot dog","hotdog","salmon","shrimp","fish","seafood","tilapia"," cod","crab","lobster","deli ","bologna"," wing","drumstick","thigh","brisket","roast","meatball","ground beef","boneless"]),
 ("Dairy & Eggs",["milk","cheese","yogurt","butter"," egg","eggs","cream cheese","sour cream","cottage","creamer","half & half","yoghurt","whipped"]),
 ("Bakery",["bread","bagel"," roll","muffin","donut","doughnut"," cake"," pie","bakery","tortilla"," bun","croissant","pastry","baguette","brownie"]),
 ("Frozen",["frozen","ice cream","popsicle","waffle","sherbet","gelato","novelties"]),
 ("Beverages",["soda","cola","pepsi","coke","sprite","bottled water","spring water","juice","lemonade","seltzer","sparkling","energy drink","gatorade","powerade","coffee"," tea "," beer"," wine","vodka","whiskey","soft drink","kombucha","water "]),
 ("Snacks & Candy",["chip","pretzel","popcorn","cracker","cookie","candy","chocolate","snack"," nuts","granola bar","fruit snack"," gum","jerky","trail mix"]),
 ("Pantry & Grocery",["cereal","pasta","rice","sauce","soup","beans","flour","sugar"," oil","mayonnaise","ketchup","mustard","condiment","pancake","syrup","peanut butter","jelly"," jam","spice","seasoning","broth","canned"," can ","noodle","oatmeal","honey","salsa","dressing","stuffing","mac & cheese","macaroni"]),
 ("Household & Paper",["paper towel","toilet paper","tissue","napkin","detergent","cleaner","cleaning","trash bag","aluminum foil","plastic wrap","storage bag","dish soap","laundry","bleach","sponge","bath tissue","ziploc"," glad "," bounty","charmin","air freshener","candle"]),
 ("Health & Beauty",["shampoo","conditioner","vitamin","supplement","medicine","tablet","capsule","toothpaste","toothbrush","deodorant"," soap","body wash","lotion","razor","shave","cosmetic","makeup","mascara","lipstick","sunscreen","pharmacy","ibuprofen","acetaminophen","allergy","cough","pain relief","first aid","feminine","skincare","serum","fragrance","perfume","hair color","nail "]),
 ("Home & Hardware",["tool","drill","paint","hardware","furniture","mattress","lumber","hose","grill","patio","lawn","garden","battery","light bulb","vacuum","cookware","appliance","kitchenware","bedding"," towel","pillow"," rug","decor","sheet set","comforter"]),
 ("Apparel & Shoes",["shirt","jean","pant","dress"," shoe","sneaker"," boot"," sock","jacket"," coat","apparel","clothing","sweater","hoodie","underwear"," bra","activewear","sandal","legging","tee "]),
 ("Electronics",[" tv ","television","laptop","headphone","earbud","iphone","tablet","console","xbox","playstation","camera","speaker","monitor","charger","electronic","smartwatch","airpod","bluetooth"]),
 ("Toys & Hobby",["toy","lego"," game","puzzle","craft"," yarn","fabric","hobby"," doll","action figure","board game"]),
]
def classify(name, cats):
    n = " "+(name or "").lower()+" "
    for dept,kws in RULES:
        for kw in kws:
            if kw in n: return dept
    # fall back on flyer category hint
    c=(cats or "").lower()
    if "grocery" in c or "food" in c: return "Pantry & Grocery"
    if "pharmac" in c or "health" in c: return "Health & Beauty"
    return "General Merchandise"

def to_float(x):
    try: return float(str(x).replace(",","").replace("$","").strip())
    except: return None

flyers=json.loads(get(f"https://backflipp.wishabi.com/flipp/flyers?locale=en-us&postal_code={POSTAL}"))["flyers"]
TODAY=datetime.date.today()
deals=[]; seen=set()
for f in flyers:
    fid=f["id"]; merch=(f.get("merchant") or "").strip()
    try:
        items=json.loads(get(f"https://backflipp.wishabi.com/flipp/flyers/{fid}?locale=en-us&postal_code={POSTAL}")).get("items",[])
    except Exception as e:
        continue
    for it in items:
        name=(it.get("name") or "").strip(); pv=to_float(it.get("price"))
        if not name or pv is None or pv<=0: continue
        key=(merch,name,round(pv,2),fid)
        if key in seen: continue
        seen.add(key)
        pre=(it.get("pre_price_text") or "").strip(); post=(it.get("post_price_text") or "").strip()
        disp=f"${pv:,.2f}"
        if pre: disp=f"{pre} {disp}"
        if post: disp=f"{disp} {post}"
        vt=(it.get("valid_to") or f.get("valid_to") or "")[:10]
        vf=(it.get("valid_from") or f.get("valid_from") or "")[:10]
        try: dl=(datetime.date.fromisoformat(vt)-TODAY).days
        except: dl=None
        deals.append({
            "s":merch,"i":name,"b":(it.get("brand") or "").strip(),
            "p":round(pv,2),"pd":disp,"u":(post or pre or ""),
            "d":classify(name, f.get("categories_csv")),
            "vt":vt,"img":it.get("cutout_image_url") or ""
        })
deals.sort(key=lambda d:(d["s"], d["d"], d["i"]))
stores=sorted(set(d["s"] for d in deals))
depts=sorted(set(d["d"] for d in deals))
meta={"generated_at":datetime.datetime.now().isoformat(timespec="seconds"),
      "generated_date":TODAY.isoformat(),
      "postal_code":POSTAL,"source":"LancasterOnline Circulars (Flipp/Wishabi API)",
      "num_deals":len(deals),"num_stores":len(stores),"stores":stores,"departments":depts}
json.dump(deals, open("/home/user/site/deals.json","w"), separators=(",",":"))
json.dump(meta, open("/home/user/site/meta.json","w"))
print("DEALS",len(deals),"STORES",len(stores),"DEPTS",len(depts))
from collections import Counter
for d,c in Counter(x["d"] for x in deals).most_common():
    print(f"  {c:>5}  {d}")
