import os
import json
import glob

import toml

ghost_post = """
{
    "id": ,
    "uuid": "b8c1d09a-be19-4b49-a7cc-c3099734df54",
    "title": "Bread2",
    "slug": "bread2",
    "markdown": "If you have less than seven hours...\n-------------------------------------\n\n...just buy it.\n\nBut, if you have seven hours...\n-------------------------------\n\n...make the **bread** yourself. \n\nGet some **bread dough** from the store.\n\n**Ingredients:**\n\n-   Bread dough\n\n**Directions:**\n\n1.  Let the bread dough rest for 20 minutes. Then knead a little bit.\n2.  Let the bread rise for 4 to 6 hours. Then flour a small bowl and put\n    loaf into bowl.\n3.  Let the bread rise again for 30 minutes, preheat a oven to 450F.\n4.  Bake the bread in a pre-heated dutch oven for 20 minutes. Take off\n    the lid and bake for another 5-10 minutes.\n5.  Take out the bread and let it rest for 20 minutes.\n\nBut, if you have seven hours and 35 minutes...\n==============================================\n\nMake the **bread dough** yourself. Get some **yeast, salt, water,\nflour** from the store. \n\n**Ingredients:**\n\n-   1 tbl. yeast\n-   760 g. water\n-   1000 g. flour\n-   20 g. salt\n\n**Directions:**\n\n-   Mix warm water and flour together. Let it rest for 20 minutes.\n-   For foccia bread, add yeast to warm water seperately.\n-   For regular bread, add yeast to the top of the dough after\n    20 minutes.\n-   Add the salt to the top of the dough and mix together.\n-   Wet hands and knead in a big bowl. Cut with fingers several times\n    and then let rest.\n\nBut, if you have ten hours...\n=============================\n\nMake the **flour** yourself. Get some **wheat berries** from the store.\n\n\n**Ingredients:**\n\n-   10 cups wheat berries\n\n**Directions:**\n\n-   Grind 1 cup of whole grain berries on the finest setting of your\n    grain mill. If you don'€™t have a grain mill, you can grind your own\n    flour using an inexpensive coffee grinder and food processor.\n-   Set the sieve over a large bowl and sift the flour. After a couple\n    minutes, you will see the germ and bran remaining in the sieve and\n    the endosperm in the bowl. Place the germ/bran into a separate\n    small bowl.\n-   Repeat with the remaining freshly ground flour until it has all\n    been sifted.\n-   Repeat the sifting process again, but this time use the flour that\n    has already been sifted. You will again see the germ/bran separate\n    in the sieve. Place the germ/bran into a separate small bowl and\n    repeat the sifting process until all the freshly ground flour has\n    been sifted twice.\n-   Store the flour and germ/bran in separate containers. The flour will\n    stay fresh in the pantry for up to one week, or you can\n    refrigerate/freeze for up to 2 months. Store the germ/bran in the\n    refrigerator or freezer for up to 2 months.\n\nBut, if you have twelve hours...\n================================\n\nMake the **wheat berries **yourself. Get some **cured wheat **from the\nstore. \n\n**Ingredients:**\n\n-   cured wheat\n-   flail\n\n**Directions:**\n\n-   Now its time to thresh the grain ' to separate the straw and chaff\n    from it. You can go about this in any number of ways. One method\n    is flailing. A flail consists of one piece of wood about 3 feet long\n    the handle attached with a leather thong to a shorter piece about 2\n    feet long.\n-   The shorter piece is flung at the heads of grain repeatedly,\n    shattering a few heads each time. If you are using this method, you\n    can expect to produce about 3 pounds of wheat in 20 to 25 minutes.\n    That's slow work. Also, there's a trick to learning to swing the\n    tail without rapping yourself on the head.\n\n<span style=\"font-size: 1.0625rem;\">The usual method for winnowing is\npouring the grain from one container to another, letting either the wind\nor the breeze from an electric fan push the lighter chaff out of the\ngrain. Repeat the process a few times to get the grain as chaff-free as\npossible.</span>\n\nBut, if you have 3 days...\n-----------------------------\n\nMake the **cured wheat** yourself.\n\nGet some **wheat** from the store.\n\n**Ingredients:**\n\n-   field of wheat\n\n**Directions:**\n\n-   As you admire your wheat stand, you'll notice in midsummer (later\n    for spring wheat) that the color of the stalks turns from green to\n    yellow or brown. The heads, heavy with grain, tip toward the earth.\n    This means it's time to test the grain. Choose a head, pick out a\n    few grains, and pop them into your mouth. If they are soft and\n    doughy, the grain is not yet ready. Keep testing. One day the grains\n    will be firm and crunchy, and it will be time to harvest.\n-   At harvest, how should you cut the wheat? If you have a small enough\n    plot, you'll just snip the heads of wheat off the stems. It goes\n    quickly if your wheat field is no larger than about 6 feet wide by\n    25 feet long.\n-   Using a scythe. If you like the old-time way of doing things and are\n    going to harvest a larger amount of grain, you might use a scythe\n    and cradle. The cradle is a series of long wooden fingers mounted\n    above the scythe blade. The scythe cuts the wheat, and then the\n    cradle carries the cut wheat to the end of each swing and deposits\n    it in a neat pile, stacked with all the heads grouped together. You\n    could cut with the scythe alone, but you would spend a lot of time\n    picking up the cut wheat and arranging it for easier handling\n-   Harvesting with a sickle. Another possible tool for cutting small\n    amounts of grain is the sickle. It's a matter of grab and cut, grab\n    and cut. Hold a handful of wheat in your left hand and swing the\n    sickle with your right to cut the plants at nearly ground level.\n    It's possible to kneel or crouch in various positions to avoid\n    getting too tired. As you cut handfuls, lay them in small piles with\n    all the heads pointed in the same direction.\n-   Binding sheaves. The next step is to bind the grain into sheaves,\n    each about 12 to 14 inches in circumference ' a bunch you can hold\n    comfortably in your hands. Bind the same day you cut the wheat. It's\n    nice to have two people taking turns cutting and binding. You can\n    bind with cord or baler's twine or even with some of the wheat\n    stems, twisting them in a way that holds the bundle firm.\n- Curing the grain. Stack sheaves\nupright in a well-ventilated, dry location safe from grain-eating\nanimals. Our ancestors stacked sheaves to make shocks in the field, but\nwith small quantities, it's easy to bring the sheaves in out of the\nweather. The grain has been cured when it is hard, shatters easily, and\ncannot be dented with your thumbnail.\n\nBut, if you have 124 days...\n============================\n\nMake the **wheat** yourself.\n\nGet some **soil, water, and sun**.\n\n**Ingredients:**\n\n-   a plot of land\n\n**Directions:**\n\n-   Plant winter wheat in fall to allow for six to eight weeks of growth\n    before the soil freezes. This allows time for good root development.\n    If the wheat is planted too early, it may smother itself the\n    following spring and it could be vulnerable to some late-summer\n    insects that won't be an issue in the cooler fall weather. If winter\n    wheat is planted too late, it will not overwinter well.\n-   Spring wheat should be planted as early as the ground can be worked\n    in spring. Do the initial plowing in the fall, then till and sow in\n    the spring. To ensure an evenly distributed crop, figure out the\n    amount of seed you'll need, divide it into two piles, and broadcast\n    one part in one direction, such as from east to west. Then broadcast\n    the remainder from north to south. A cyclone crank seeder will do an\n    even job, but broadcasting by hand is fine for a small plot. You\n    also can plant it in rows like other crops.\n-   Cover the seed by rototilling or raking it in to a depth of 2 to 2\n    1'2 inches for winter wheat and 1 to 1 1'2 inches for spring wheat.\n    For best results, roll or otherwise firm the bed to ensure good\n    seed-soil contact.\n\n",
    "mobiledoc": null,
    "html": "<h2 id=\"ifyouhavelessthansevenhours\">If you have less than seven hours...  </h2>\n\n<p>...just buy it.</p>\n\n<h2 id=\"butifyouhavesevenhours\">But, if you have seven hours...  </h2>\n\n<p>...make the <strong>bread</strong> yourself. </p>\n\n<p>Get some <strong>bread dough</strong> from the store.</p>\n\n<p><strong>Ingredients:</strong></p>\n\n<ul>\n<li>Bread dough</li>\n</ul>\n\n<p><strong>Directions:</strong></p>\n\n<ol>\n<li>Let the bread dough rest for 20 minutes. Then knead a little bit.  </li>\n<li>Let the bread rise for 4 to 6 hours. Then flour a small bowl and put <br />\nloaf into bowl.</li>\n<li>Let the bread rise again for 30 minutes, preheat a oven to 450F.  </li>\n<li>Bake the bread in a pre-heated dutch oven for 20 minutes. Take off <br />\nthe lid and bake for another 5-10 minutes.</li>\n<li>Take out the bread and let it rest for 20 minutes.</li>\n</ol>\n\n<h1 id=\"butifyouhavesevenhoursand35minutes\">But, if you have seven hours and 35 minutes...  </h1>\n\n<p>Make the <strong>bread dough</strong> yourself. Get some <strong>yeast, salt, water, <br />\nflour</strong> from the store. </p>\n\n<p><strong>Ingredients:</strong></p>\n\n<ul>\n<li>1 tbl. yeast</li>\n<li>760 g. water</li>\n<li>1000 g. flour</li>\n<li>20 g. salt</li>\n</ul>\n\n<p><strong>Directions:</strong></p>\n\n<ul>\n<li>Mix warm water and flour together. Let it rest for 20 minutes.</li>\n<li>For foccia bread, add yeast to warm water seperately.</li>\n<li>For regular bread, add yeast to the top of the dough after\n20 minutes.</li>\n<li>Add the salt to the top of the dough and mix together.</li>\n<li>Wet hands and knead in a big bowl. Cut with fingers several times\nand then let rest.</li>\n</ul>\n\n<h1 id=\"butifyouhavetenhours\">But, if you have ten hours...  </h1>\n\n<p>Make the <strong>flour</strong> yourself. Get some <strong>wheat berries</strong> from the store.</p>\n\n<p><strong>Ingredients:</strong></p>\n\n<ul>\n<li>10 cups wheat berries</li>\n</ul>\n\n<p><strong>Directions:</strong></p>\n\n<ul>\n<li>Grind 1 cup of whole grain berries on the finest setting of your\ngrain mill. If you don'€™t have a grain mill, you can grind your own\nflour using an inexpensive coffee grinder and food processor.</li>\n<li>Set the sieve over a large bowl and sift the flour. After a couple\nminutes, you will see the germ and bran remaining in the sieve and\nthe endosperm in the bowl. Place the germ/bran into a separate\nsmall bowl.</li>\n<li>Repeat with the remaining freshly ground flour until it has all\nbeen sifted.</li>\n<li>Repeat the sifting process again, but this time use the flour that\nhas already been sifted. You will again see the germ/bran separate\nin the sieve. Place the germ/bran into a separate small bowl and\nrepeat the sifting process until all the freshly ground flour has\nbeen sifted twice.</li>\n<li>Store the flour and germ/bran in separate containers. The flour will\nstay fresh in the pantry for up to one week, or you can\nrefrigerate/freeze for up to 2 months. Store the germ/bran in the\nrefrigerator or freezer for up to 2 months.</li>\n</ul>\n\n<h1 id=\"butifyouhavetwelvehours\">But, if you have twelve hours...  </h1>\n\n<p>Make the <em>*wheat berries *</em>yourself. Get some <em>*cured wheat *</em>from the <br />\nstore. </p>\n\n<p><strong>Ingredients:</strong></p>\n\n<ul>\n<li>cured wheat</li>\n<li>flail</li>\n</ul>\n\n<p><strong>Directions:</strong></p>\n\n<ul>\n<li>Now its time to thresh the grain ' to separate the straw and chaff\nfrom it. You can go about this in any number of ways. One method\nis flailing. A flail consists of one piece of wood about 3 feet long\nthe handle attached with a leather thong to a shorter piece about 2\nfeet long.</li>\n<li>The shorter piece is flung at the heads of grain repeatedly,\nshattering a few heads each time. If you are using this method, you\ncan expect to produce about 3 pounds of wheat in 20 to 25 minutes.\nThat's slow work. Also, there's a trick to learning to swing the\ntail without rapping yourself on the head.</li>\n</ul>\n\n<p><span style=\"font-size: 1.0625rem;\">The usual method for winnowing is <br />\npouring the grain from one container to another, letting either the wind <br />\nor the breeze from an electric fan push the lighter chaff out of the <br />\ngrain. Repeat the process a few times to get the grain as chaff-free as <br />\npossible.</span></p>\n\n<h2 id=\"butifyouhave3days\">But, if you have 3 days...  </h2>\n\n<p>Make the <strong>cured wheat</strong> yourself.</p>\n\n<p>Get some <strong>wheat</strong> from the store.</p>\n\n<p><strong>Ingredients:</strong></p>\n\n<ul>\n<li>field of wheat</li>\n</ul>\n\n<p><strong>Directions:</strong></p>\n\n<ul>\n<li>As you admire your wheat stand, you'll notice in midsummer (later\nfor spring wheat) that the color of the stalks turns from green to\nyellow or brown. The heads, heavy with grain, tip toward the earth.\nThis means it's time to test the grain. Choose a head, pick out a\nfew grains, and pop them into your mouth. If they are soft and\ndoughy, the grain is not yet ready. Keep testing. One day the grains\nwill be firm and crunchy, and it will be time to harvest.</li>\n<li>At harvest, how should you cut the wheat? If you have a small enough\nplot, you'll just snip the heads of wheat off the stems. It goes\nquickly if your wheat field is no larger than about 6 feet wide by\n25 feet long.</li>\n<li>Using a scythe. If you like the old-time way of doing things and are\ngoing to harvest a larger amount of grain, you might use a scythe\nand cradle. The cradle is a series of long wooden fingers mounted\nabove the scythe blade. The scythe cuts the wheat, and then the\ncradle carries the cut wheat to the end of each swing and deposits\nit in a neat pile, stacked with all the heads grouped together. You\ncould cut with the scythe alone, but you would spend a lot of time\npicking up the cut wheat and arranging it for easier handling</li>\n<li>Harvesting with a sickle. Another possible tool for cutting small\namounts of grain is the sickle. It's a matter of grab and cut, grab\nand cut. Hold a handful of wheat in your left hand and swing the\nsickle with your right to cut the plants at nearly ground level.\nIt's possible to kneel or crouch in various positions to avoid\ngetting too tired. As you cut handfuls, lay them in small piles with\nall the heads pointed in the same direction.</li>\n<li>Binding sheaves. The next step is to bind the grain into sheaves,\neach about 12 to 14 inches in circumference ' a bunch you can hold\ncomfortably in your hands. Bind the same day you cut the wheat. It's\nnice to have two people taking turns cutting and binding. You can\nbind with cord or baler's twine or even with some of the wheat\nstems, twisting them in a way that holds the bundle firm.</li>\n<li>Curing the grain. Stack sheaves\nupright in a well-ventilated, dry location safe from grain-eating <br />\nanimals. Our ancestors stacked sheaves to make shocks in the field, but <br />\nwith small quantities, it's easy to bring the sheaves in out of the <br />\nweather. The grain has been cured when it is hard, shatters easily, and <br />\ncannot be dented with your thumbnail.</li>\n</ul>\n\n<h1 id=\"butifyouhave124days\">But, if you have 124 days...  </h1>\n\n<p>Make the <strong>wheat</strong> yourself.</p>\n\n<p>Get some <strong>soil, water, and sun</strong>.</p>\n\n<p><strong>Ingredients:</strong></p>\n\n<ul>\n<li>a plot of land</li>\n</ul>\n\n<p><strong>Directions:</strong></p>\n\n<ul>\n<li>Plant winter wheat in fall to allow for six to eight weeks of growth\nbefore the soil freezes. This allows time for good root development.\nIf the wheat is planted too early, it may smother itself the\nfollowing spring and it could be vulnerable to some late-summer\ninsects that won't be an issue in the cooler fall weather. If winter\nwheat is planted too late, it will not overwinter well.</li>\n<li>Spring wheat should be planted as early as the ground can be worked\nin spring. Do the initial plowing in the fall, then till and sow in\nthe spring. To ensure an evenly distributed crop, figure out the\namount of seed you'll need, divide it into two piles, and broadcast\none part in one direction, such as from east to west. Then broadcast\nthe remainder from north to south. A cyclone crank seeder will do an\neven job, but broadcasting by hand is fine for a small plot. You\nalso can plant it in rows like other crops.</li>\n<li>Cover the seed by rototilling or raking it in to a depth of 2 to 2\n1'2 inches for winter wheat and 1 to 1 1'2 inches for spring wheat.\nFor best results, roll or otherwise firm the bed to ensure good\nseed-soil contact.</li>\n</ul>",
    "amp": null,
    "image": "http://www.smallfriendly.com/.a/6a0133ec490e97970b017ee99b0136970d-800wi",
    "featured": 0,
    "page": 0,
    "status": "published",
    "language": "en_US",
    "visibility": "public",
    "meta_title": "Making bread in 124 days",
    "meta_description": "How to make bread from its essential ingredients: wheat.",
    "author_id": 1,
    "created_at": "2017-01-18 20:57:46",
    "created_by": 1,
    "updated_at": "2017-01-18 22:02:38",
    "updated_by": 1,
    "published_at": "2017-01-18 20:57:47",
    "published_by": 1
}
"""

ghost_tag = """
{
    "id": 50,
    "uuid": "99c7f68f-4657-4760-a956-a53d266a27b8",
    "name": "bready",
    "slug": "bready",
    "description": null,
    "image": null,
    "parent_id": null,
    "visibility": "public",
    "meta_title": null,
    "meta_description": null,
    "created_at": "2017-01-18 21:54:51",
    "created_by": 1,
    "updated_at": "2017-01-18 21:54:51",
    "updated_by": 1
}
"""

ghost_post_tag = """
{
    "id": 67687,
    "post_id": 345,
    "tag_id": 50,
    "sort_order": 3
}
"""

ghost_json ="""
{
    "db": [
        {
            "data": {
                "posts": [
                ],
                "tags": [
                ],
                "posts_tags": [
                ]
            }
        }
    ]
}
"""

product_reactions = {}  # dictionary of product -> list of reactions that contains that product
reactions = [] # all reactions
for filename in glob.iglob('data/**/*.toml', recursive=True):
    print(filename)
    with open(filename) as conffile:
        config = toml.loads(conffile.read())
        print(config)
        for reaction in config['reaction']:
            for product in reaction['products']:
                if product not in product_reactions:
                    product_reactions[product] = []
                product_reactions[product].append(reaction)
            reactions.append(reaction)

print(json.dumps(product_reactions,indent=2))



graphviz = ["digraph G {\n"]
for reaction in reactions:
    graphviz.append("\t{ " + " ".join(reaction['reactants']) + "} -> { " + " ".join(reaction['products']) + " };\n")
graphviz.append("}")

with open("graphviz","w") as f:
    f.write("".join(graphviz))

os.system("dot -O -Tpng graphviz")
os.remove("graphviz")
