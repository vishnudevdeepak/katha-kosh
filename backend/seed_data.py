"""
Seed script for Kathā-Kosh database.
Run from backend/ directory: python seed_data.py

Populates the database with 25+ real Indian heritage records.
"""
import sys
import os

# Ensure the backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.heritage_item import HeritageItem
from app.models.user import User
from app.services.auth_service import hash_password

Base.metadata.create_all(bind=engine)

ITEMS = [
    {
        "title": "Aranmula Kannadi",
        "slug": "aranmula-kannadi",
        "description": (
            "The Aranmula Kannadi is a unique metal mirror crafted in Aranmula village, Kerala, "
            "by artisans of the Vishwakarma community using a secret bell-metal alloy whose exact "
            "composition has never been disclosed. Unlike glass mirrors, it reflects a true image "
            "without any secondary reflection, giving it extraordinary clarity."
        ),
        "type": "metalwork",
        "region": "South India",
        "state": "Kerala",
        "district": "Pathanamthitta",
        "language": "Malayalam",
        "community": "Vishwakarma",
        "historical_period": "Pre-18th century",
        "cultural_significance": (
            "The mirror is one of the eight auspicious items (Ashtamangalyam) used in traditional "
            "Kerala ceremonies, including weddings and temple rituals. It holds deep ritual significance "
            "and is offered to the Parthasarathy temple in Aranmula as part of the Uthrattadi festival."
        ),
        "traditional_technique": (
            "Cast using a secret alloy of copper, tin, and other metals through the lost-wax (cire perdue) "
            "process. The mirror surface is hand-polished to a reflective finish without any glass coating."
        ),
        "why_it_matters": (
            "One of only two metal-mirror traditions in the world still in production. "
            "GI-tagged by the Government of India, protecting its unique regional identity."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Vishwakarma community artisans, Aranmula",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/55/Aranmula_mirror_high_quality_bronze_mirror.jpg",
        "tags": "metal,mirror,bell-metal,GI-tag,ritual,ashtamangalyam,Kerala",
        "sources": "Geographical Indications Registry of India; Kerala Folklore Academy",
        "status": "published",
    },
    {
        "title": "Vadakkan Pattukal",
        "slug": "vadakkan-pattukal",
        "description": (
            "Vadakkan Pattukal are heroic ballads from northern Kerala recounting the lives and deeds "
            "of warrior heroes such as Thacholi Othenan, Aromal Chekavar, and Unniyarcha. These oral "
            "epics were traditionally performed by bards at community gatherings and martial training arenas (kalaris)."
        ),
        "type": "folk_story",
        "region": "North Kerala",
        "state": "Kerala",
        "district": "Kozhikode",
        "language": "Malayalam",
        "community": "Nair",
        "historical_period": "16th–18th century",
        "cultural_significance": (
            "The ballads document the martial traditions, social codes, and ethical values of medieval "
            "Malabar society. They served as moral guidelines for warrior communities and preserved memory "
            "of regional heroes who resisted social injustice."
        ),
        "traditional_technique": (
            "Oral transmission through generations of professional bards (Panas) who memorised thousands "
            "of verses and performed them with minimal musical accompaniment."
        ),
        "why_it_matters": (
            "Vadakkan Pattukal is a primary source for understanding the martial arts tradition of Kalaripayattu "
            "and the social fabric of pre-colonial northern Kerala."
        ),
        "preservation_status": "endangered",
        "artisan": "Traditional bards (Pana community)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Boys_at_Kalaripayattu_class.jpg/1280px-Boys_at_Kalaripayattu_class.jpg",
        "tags": "ballad,oral-tradition,warrior,Malabar,Malayalam,medieval,kalaripayattu",
        "sources": "Kerala Sahitya Akademi; M.V. Vishnu Namboodiri (scholar)",
        "status": "published",
    },
    {
        "title": "Channapatna Toys",
        "slug": "channapatna-toys",
        "description": (
            "Channapatna toys are brightly lacquered wooden toys produced in the town of Channapatna "
            "in Karnataka. Using ivory wood (aale mara) and natural lac dyes, artisans create dolls, "
            "spinning tops, rattles, and figurines in vivid colours. The town is popularly known as "
            "'Toy Town' of Karnataka."
        ),
        "type": "woodwork",
        "region": "South India",
        "state": "Karnataka",
        "district": "Ramanagara",
        "language": "Kannada",
        "community": "Toy-maker guilds of Channapatna",
        "historical_period": "18th century",
        "cultural_significance": (
            "The craft was patronised by Tipu Sultan, who invited craftsmen from Persia to train local "
            "artisans in the lacquerware technique. This cultural exchange produced a distinctive style "
            "that blends Persian craftsmanship with local Indian sensibility."
        ),
        "traditional_technique": (
            "Soft ivory wood is turned on a lathe; lac sticks are applied by hand while the wood spins, "
            "building up layers of colour. No synthetic dyes are used; colour comes from natural lac "
            "impregnated with vegetable pigments."
        ),
        "why_it_matters": (
            "GI-tagged, eco-friendly, and child-safe. Channapatna toys represent the viability of "
            "traditional craft as sustainable livelihood in modern markets."
        ),
        "preservation_status": "thriving",
        "artisan": "Toy-maker guilds, Channapatna",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Channapatna_toys06.jpg/1280px-Channapatna_toys06.jpg",
        "tags": "wood,lacquer,toy,GI-tag,Karnataka,Tipu-Sultan,eco-friendly",
        "sources": "Karnataka Handicrafts Development Corporation; GI Registry",
        "status": "published",
    },
    {
        "title": "Phad Painting",
        "slug": "phad-painting",
        "description": (
            "Phad is a large-format narrative scroll painting from Shahpura in Rajasthan, painted on "
            "specially treated cloth using natural mineral and vegetable colours. Each phad depicts "
            "episodes from the epics of local folk-deities Pabuji or Devnarayan and can extend up to "
            "30 feet in length."
        ),
        "type": "folk_art",
        "region": "Rajasthan",
        "state": "Rajasthan",
        "district": "Bhilwara",
        "language": "Rajasthani",
        "community": "Joshi (Chipa) community",
        "historical_period": "14th century onwards",
        "cultural_significance": (
            "The phad served as a portable temple — Bhopa priests (Nayak community) would unroll the "
            "phad at night and sing the epic of Pabuji by lamplight, using the painting as a visual "
            "aid. The painting and the oral performance are inseparable ritual acts."
        ),
        "traditional_technique": (
            "Cloth is prepared with a mixture of rice starch and chalk powder, then polished with stone. "
            "Outlines are drawn in black, and flat vegetal colours are applied in a strict sequential order."
        ),
        "why_it_matters": (
            "Phad keeps alive the oral epic traditions of Rajasthan's pastoral communities. "
            "Its makers (the Joshi family of Shahpura) have been recognised with national awards."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Joshi family, Shahpura",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/23/Stamp_of_India_-_1992_-_Colnect_164323_-_Phad_Scroll_Paintings_from_Rajasthan.jpeg",
        "tags": "painting,scroll,folk-deity,Bhopa,Pabuji,Rajasthan,natural-colour",
        "sources": "Rajasthan Lalit Kala Akademi; National Crafts Museum, New Delhi",
        "status": "published",
    },
    {
        "title": "Warli Painting",
        "slug": "warli-painting",
        "description": (
            "Warli painting is a tribal art form originating in the Warli tribe of the Maharashtra–Gujarat "
            "border region. Artists use white pigment made from rice paste on a red-ochre background to "
            "create compositions built entirely from geometric shapes: circles, triangles, and squares."
        ),
        "type": "folk_art",
        "region": "Western India",
        "state": "Maharashtra",
        "district": "Palghar",
        "language": "Warli",
        "community": "Warli tribe",
        "historical_period": "Pre-10th century CE",
        "cultural_significance": (
            "Warli paintings are ritualistic objects; the central motif — the 'Tarpa dance' circle — "
            "represents the cycle of creation. They are painted on the walls of homes during harvests, "
            "weddings, and festivals to invite the goddess Palaghata's blessings."
        ),
        "traditional_technique": (
            "White pigment from rice paste, water, and gum is applied with a bamboo twig chewed at one end "
            "to form a fine brush. Compositions depict the village ecosystem: farming, hunting, nature spirits."
        ),
        "why_it_matters": (
            "One of the oldest surviving tribal art forms in India, Warli art has evolved into a globally "
            "recognised contemporary art movement while retaining its ritual roots."
        ),
        "preservation_status": "thriving",
        "artisan": "Warli community artists, Palghar district",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Warli_art.jpg/1280px-Warli_art.jpg",
        "tags": "tribal,geometric,nature,Maharashtra,white-pigment,ritual,circle",
        "sources": "Tribal Research Institute, Maharashtra; Bhau Daji Lad Museum",
        "status": "published",
    },
    {
        "title": "Pattachitra",
        "slug": "pattachitra",
        "description": (
            "Pattachitra is a traditional cloth-based scroll painting from Puri and Raghurajpur village "
            "in Odisha. The name derives from Sanskrit 'patta' (cloth) and 'chitra' (picture). Artists "
            "depict scenes from Hindu mythology — especially the legend of Jagannath — using natural "
            "colours derived from minerals, plants, and lamp black."
        ),
        "type": "folk_art",
        "region": "East India",
        "state": "Odisha",
        "district": "Puri",
        "language": "Odia",
        "community": "Chitrakara community",
        "historical_period": "12th century",
        "cultural_significance": (
            "Pattachitra paintings are intimately linked to the Jagannath temple culture at Puri; "
            "they serve as portable icons of the deity and are sold as ritual souvenirs to pilgrims. "
            "The village of Raghurajpur has been designated a heritage crafts village."
        ),
        "traditional_technique": (
            "Layers of cotton cloth are bonded with chalk and tamarind paste to create 'patta'. "
            "Natural pigments from conch shells (white), indigo (blue), haritala (yellow), and "
            "vermillion (red) are used. All outlines are drawn freehand in black."
        ),
        "why_it_matters": (
            "GI-tagged, Pattachitra has been practised for nearly 1,000 years and remains a living "
            "tradition supporting over 100 families in Raghurajpur alone."
        ),
        "preservation_status": "thriving",
        "artisan": "Chitrakara community, Raghurajpur",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Odisha_Pattachitara_Depicting_Unconditional_Love_between_Radha_Krushna.jpg",
        "tags": "cloth,natural-colour,Jagannath,mythology,GI-tag,Odisha,scroll",
        "sources": "Odisha Lalit Kala Akademi; GI Registry of India",
        "status": "published",
    },
    {
        "title": "Madhubani Painting",
        "slug": "madhubani-painting",
        "description": (
            "Madhubani (Mithila) painting is a centuries-old art tradition practised by women in the "
            "Mithila region of Bihar. Executed on freshly plastered mud walls or handmade paper using "
            "fingers, twigs, brushes, and matchsticks, it depicts Hindu deities, nature, and royal court "
            "scenes in bold lines and vivid natural colours."
        ),
        "type": "folk_art",
        "region": "East India",
        "state": "Bihar",
        "district": "Madhubani",
        "language": "Maithili",
        "community": "Brahmin and Kayastha women of Mithila",
        "historical_period": "Ancient; documented since the Ramayana era",
        "cultural_significance": (
            "Madhubani painting was traditionally created for auspicious occasions — weddings, births, "
            "and festivals — to invoke divine blessings. Post the 1934 earthquake, the government encouraged "
            "women to paint on paper, transforming a wall tradition into a commercial art form."
        ),
        "traditional_technique": (
            "Natural dyes from turmeric, indigo, kohl, sandalwood, and crushed flowers are used. "
            "No space is left blank — every inch is filled with geometric fillers and patterns."
        ),
        "why_it_matters": (
            "GI-tagged. Madhubani art gave economic agency to rural women of Bihar and has been exhibited "
            "in galleries worldwide, from New York to Tokyo."
        ),
        "preservation_status": "thriving",
        "artisan": "Women artists of Mithila region",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Asha_Jha_Madhubani_Painting_Bihar_Artist.jpg",
        "tags": "Mithila,women,natural-dye,GI-tag,Bihar,deity,ritual,Maithili",
        "sources": "Bihar State Handicrafts Development Corporation; National Crafts Museum",
        "status": "published",
    },
    {
        "title": "Dokra Metal Craft",
        "slug": "dokra-metal-craft",
        "description": (
            "Dokra is a non-ferrous metal casting technique using the lost-wax (cire perdue) process, "
            "practised by tribal communities across West Bengal, Chhattisgarh, Jharkhand, and Odisha. "
            "Over 4,000 years old, it is among the oldest metal casting traditions in the world — "
            "a dancing girl figurine from Mohenjo-daro is believed to be an early example."
        ),
        "type": "metalwork",
        "region": "East India",
        "state": "West Bengal",
        "district": "Bankura",
        "language": "Bengali",
        "community": "Dhokra Damar tribes",
        "historical_period": "Over 4,000 years",
        "cultural_significance": (
            "Dokra figurines — horses, elephants, tribal deities, lamps, and domestic objects — are "
            "used in tribal religious ceremonies and as votive offerings. The craft embodies a continuous "
            "cultural memory stretching back to the Indus Valley Civilisation."
        ),
        "traditional_technique": (
            "A clay core is shaped and coated with beeswax threads sculpted into the final design. "
            "This is encased in clay and fired; the wax melts out (lost wax) and molten brass is poured in. "
            "Each piece is unique because the clay mould is broken to release the casting."
        ),
        "why_it_matters": (
            "One of the world's oldest surviving metal casting traditions; each piece is unrepeatable. "
            "Dokra supports the livelihoods of marginalised tribal families across four states."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Dhokra Damar community",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Dancing_girl_of_Mohenjo-daro.jpg",
        "tags": "lost-wax,tribal,ancient,brass,Indus-Valley,cire-perdue,Bengal",
        "sources": "Crafts Council of West Bengal; National Museum, New Delhi",
        "status": "published",
    },
    {
        "title": "Thanjavur Painting",
        "slug": "thanjavur-painting",
        "description": (
            "Thanjavur painting is a classical South Indian painting style originating in the town of "
            "Thanjavur (Tanjore) in Tamil Nadu. Known for their rich, vivid colours and characteristic "
            "gold-foil work, the paintings depict Hindu deities set against elaborate decorative "
            "backgrounds embedded with semi-precious stones and glass."
        ),
        "type": "folk_art",
        "region": "South India",
        "state": "Tamil Nadu",
        "district": "Thanjavur",
        "language": "Tamil",
        "community": "Raju community artists",
        "historical_period": "16th century (Nayaka period)",
        "cultural_significance": (
            "Thanjavur paintings were created as devotional objects for temples and royal courts during "
            "the Nayaka period. They embody the theological aesthetics of South Indian Vaishnavism and "
            "Shaivism and continue to be used as domestic shrine objects."
        ),
        "traditional_technique": (
            "Chalk powder and gum arabic are mixed to create a paste for the base relief. Gold leaf "
            "is applied over the embossed areas. Natural colours — cadmium, ultramarine — provide depth. "
            "The process can take weeks for a single panel."
        ),
        "why_it_matters": (
            "GI-tagged. Thanjavur painting represents the apex of the Deccan painting tradition and "
            "continues to be an important ritual and devotional art form in Tamil Nadu."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Raju and Chettiar families, Thanjavur",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Thanjavur_art_from_south_India.jpg",
        "tags": "gold-foil,deity,classical,Chola,Nayaka,GI-tag,Tamil-Nadu,semi-precious",
        "sources": "Tamil Nadu Handicrafts Development Corporation; GI Registry",
        "status": "published",
    },
    {
        "title": "Kantha Embroidery",
        "slug": "kantha-embroidery",
        "description": (
            "Kantha is a form of embroidery from West Bengal and Bangladesh using layers of old, "
            "discarded saris stitched together with a simple running stitch called 'kantha'. "
            "The layered cloth is transformed into quilts, bedspreads, shawls, and wraps adorned "
            "with folk motifs: lotus, fish, birds, and geometric patterns."
        ),
        "type": "textile",
        "region": "East India",
        "state": "West Bengal",
        "district": "Murshidabad",
        "language": "Bengali",
        "community": "Rural women of West Bengal",
        "historical_period": "Pre-18th century",
        "cultural_significance": (
            "Kantha was originally a domestic craft: women recycled old saris into useful items for "
            "their families. The layers of cloth and stitches carry symbolic meaning — the running "
            "stitch represents the flow of water and the continuity of life."
        ),
        "traditional_technique": (
            "Three to seven layers of sari cloth are aligned and tacked together. A running stitch — "
            "the kantha stitch — is worked across the entire surface, drawing out folk motifs from "
            "the natural warp and weft of the fabric."
        ),
        "why_it_matters": (
            "GI-tagged. Kantha is a profound example of sustainable craft — transforming discarded "
            "textiles into valuable art — while empowering rural women economically."
        ),
        "preservation_status": "thriving",
        "artisan": "Women artisans, Murshidabad and Nadia districts",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a3/Nakshi_Kantha_craftswoman.jpg",
        "tags": "stitch,quilt,folk-motif,GI-tag,West-Bengal,running-stitch,upcycling",
        "sources": "West Bengal Khadi & Village Industries Board; GI Registry",
        "status": "published",
    },
    {
        "title": "Kashmiri Pashmina",
        "slug": "kashmiri-pashmina",
        "description": (
            "Pashmina is a luxury textile woven from the ultra-fine wool of the Changthangi goat, "
            "found at altitudes above 14,000 feet in the Changthang plateau of Ladakh. A single "
            "Pashmina shawl may require the wool of three goats and months of hand-spinning and "
            "hand-weaving on a wooden loom."
        ),
        "type": "textile",
        "region": "North India",
        "state": "Jammu & Kashmir",
        "district": "Srinagar",
        "language": "Kashmiri",
        "community": "Kashmiri weavers; Changpa nomads",
        "historical_period": "15th century (Zayn-ul-Abidin era)",
        "cultural_significance": (
            "Pashmina shawls have been diplomatic gifts between Mughal emperors, European royalty, "
            "and heads of state for centuries. The Kani shawl technique, using wooden bobbins, "
            "produces intricate tapestry patterns that read like woven paintings."
        ),
        "traditional_technique": (
            "Changthangi goat wool is hand-combed by nomadic Changpa women, then hand-spun on a "
            "spinning wheel (yinder). The yarn is woven on traditional wooden looms (kani loom for "
            "tapestry weaves); embroidery (sozni) is added by hand with an extremely fine needle."
        ),
        "why_it_matters": (
            "GI-tagged as 'Kashmir Pashmina'. Faces severe threats from machine-made imitations "
            "and climate change impacting Changthangi goat populations."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Kashmiri weaver families; Changpa nomads, Ladakh",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Mandala_Chandar%2C_Kashmir_1840.jpg",
        "tags": "wool,luxury,hand-woven,GI-tag,Kashmir,Ladakh,Kani,Changthangi",
        "sources": "Craft Development Institute, Srinagar; GI Registry",
        "status": "published",
    },
    {
        "title": "Bidriware",
        "slug": "bidriware",
        "description": (
            "Bidriware is a unique metal handicraft from Bidar, Karnataka, characterised by its "
            "distinctive matte-black surface of a zinc–copper alloy inlaid with pure silver. "
            "The name comes from the town of Bidar, where the craft originated under the Bahmani "
            "Sultanate in the 14th century."
        ),
        "type": "metalwork",
        "region": "South India",
        "state": "Karnataka",
        "district": "Bidar",
        "language": "Urdu / Kannada",
        "community": "Sultani community artisans",
        "historical_period": "14th century (Bahmani Sultanate)",
        "cultural_significance": (
            "Bidriware reached its artistic zenith under Mughal patronage and was gifted to European "
            "trading companies and royal courts. The black finish is achieved using soil unique to "
            "the fort of Bidar — no other soil in the world produces this oxidation."
        ),
        "traditional_technique": (
            "An alloy of zinc, copper, lead, and tin is cast and shaped. Silver wire is hammered "
            "into engraved grooves (inlay) or laid on the surface (overlay). The piece is then "
            "oxidised with a paste of ammonium chloride and soil from Bidar fort."
        ),
        "why_it_matters": (
            "GI-tagged. The oxidising soil is found only within the Bidar fort complex, making "
            "this craft geographically irreplaceable. Bidriware represents a synthesis of Persian, "
            "Mughal, and Deccan aesthetic traditions."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Sultani artisan community, Bidar",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/12/Bidriware_Hookah.jpg",
        "tags": "zinc,silver-inlay,Bidar,Mughal-era,GI-tag,Karnataka,Bahmani",
        "sources": "Karnataka Handicrafts Development Corporation; GI Registry",
        "status": "published",
    },
    {
        "title": "Rogan Art",
        "slug": "rogan-art",
        "description": (
            "Rogan art is an extremely rare form of cloth painting from Nirona village in Kutch, "
            "Gujarat, in which a castor-oil-based thick paint is worked on fabric using a metal "
            "rod — the paint never touches the cloth directly but is stretched into fine threads "
            "and laid onto the surface with breath-like precision."
        ),
        "type": "folk_art",
        "region": "Western India",
        "state": "Gujarat",
        "district": "Kutch",
        "language": "Kutchi",
        "community": "Khatri family, Nirona",
        "historical_period": "17th century",
        "cultural_significance": (
            "Rogan art was famously gifted by Prime Minister Modi to US President Barack Obama and "
            "was originally brought from Persia. Today only the Khatri family of Nirona practises "
            "this art, making it one of the rarest living crafts on earth."
        ),
        "traditional_technique": (
            "Castor oil is boiled for hours into a viscous paste and mixed with natural pigments. "
            "Using a metal stylus, the artist stretches threads of this paint into intricate "
            "symmetrical patterns on cloth using a folding technique to mirror designs."
        ),
        "why_it_matters": (
            "Only one family in the world practises this art form. It represents the extreme edge "
            "of endangered intangible heritage and raises urgent questions about monoculture preservation."
        ),
        "preservation_status": "critically_endangered",
        "artisan": "Khatri family, Nirona village, Kutch",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/32/Rogan-art-Tree-of-Life-Abdul-Gafur-Khatri-29-12-2013.jpg",
        "tags": "castor-oil,Kutch,endangered,rare,Gujarat,Persian-origin,Khatri",
        "sources": "Crafts Council of India; Gujarat Livelihoods Foundation",
        "status": "published",
    },
    {
        "title": "Dhokra Craft of Bastar",
        "slug": "dhokra-craft-bastar",
        "description": (
            "The bell-metal craft of Bastar in Chhattisgarh is a form of Dokra craftsmanship unique "
            "to the tribal communities of this region. Using a variation of the lost-wax technique, "
            "artisans create figurines of tribal deities, ritual objects, animals, and ceremonial "
            "lamps with distinctive linear decorations."
        ),
        "type": "metalwork",
        "region": "Central India",
        "state": "Chhattisgarh",
        "district": "Bastar",
        "language": "Halbi / Gondi",
        "community": "Ghadwa tribal community",
        "historical_period": "Pre-16th century",
        "cultural_significance": (
            "Bastar bell-metal objects are essential in tribal ritual contexts: lamps (deepak), "
            "ceremonial staffs, and votive animals are offered at village deities' shrines. "
            "The craft encodes tribal cosmology and spiritual belief systems."
        ),
        "traditional_technique": (
            "Local clay is mixed with cow dung and rice husk to form cores. Beeswax strips are "
            "wound around and carved into decorative patterns before encasing in clay. "
            "Bell metal (copper–tin alloy) is poured into the fired mould."
        ),
        "why_it_matters": (
            "Bastar Dhokra represents a living technological tradition of the Indus Valley era. "
            "Its practitioners are among India's most marginalised communities whose cultural "
            "heritage deserves urgent documentation and support."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Ghadwa community, Bastar",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Shiva_as_the_Lord_of_Dance_LACMA_edit.jpg",
        "tags": "tribal,bell-metal,Bastar,ritual,Chhattisgarh,lost-wax,Ghadwa",
        "sources": "Tribal Welfare Department, Chhattisgarh; Crafts Museum New Delhi",
        "status": "published",
    },
    {
        "title": "Khamba Thoibi Dance",
        "slug": "khamba-thoibi-dance",
        "description": (
            "Khamba Thoibi is a classical dance form of the Meitei people of Manipur, performed as "
            "part of the Lai Haraoba festival. It enacts the love story of the folk hero Khamba and "
            "the princess Thoibi — a central narrative in Meitei cultural mythology."
        ),
        "type": "dance",
        "region": "Northeast India",
        "state": "Manipur",
        "district": "Imphal",
        "language": "Meitei (Manipuri)",
        "community": "Meitei",
        "historical_period": "Pre-15th century",
        "cultural_significance": (
            "The dance is an integral part of Lai Haraoba, the most important pre-Hindu festival "
            "of the Meitei people, connecting communities to their indigenous religious traditions "
            "and cosmological beliefs preserved before the advent of Vaishnavism."
        ),
        "traditional_technique": (
            "Performed by male and female duets in elaborate silk costumes. Movement vocabulary "
            "combines slow, graceful gestures with ritualistic sequences guided by the Maibas "
            "(priests) and Maibis (priestesses) of the community."
        ),
        "why_it_matters": (
            "One of the most ancient performing traditions of Northeast India, Khamba Thoibi "
            "is a cultural anchor for Meitei identity and an expression of indigenous Manipuri theology."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Meitei Maibis (female ritualists) and trained dancers",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Lai_Haraoba-3_-_5571676820.jpg",
        "tags": "Meitei,festival,agricultural,oral-tradition,Manipur,Lai-Haraoba,classical",
        "sources": "Sangeet Natak Akademi; Manipur State Kala Akademi",
        "status": "published",
    },
    {
        "title": "Bihu Dance",
        "slug": "bihu-dance",
        "description": (
            "Bihu is a vibrant folk dance of Assam associated with the three Bihu festivals: "
            "Rongali (spring/new year), Kongali (autumn), and Bhogali (winter harvest). "
            "Rongali Bihu features energetic, uninhibited dancing by young men and women "
            "in open fields, expressing joy, fertility, and the renewal of life."
        ),
        "type": "dance",
        "region": "Northeast India",
        "state": "Assam",
        "district": "Kamrup",
        "language": "Assamese",
        "community": "Assamese community broadly",
        "historical_period": "Pre-7th century CE",
        "cultural_significance": (
            "Bihu transcends caste, community, and religion to serve as the defining cultural "
            "identity of Assam. The dance, songs, and music celebrate the agrarian cycle and "
            "the intimate relationship between Assamese people and the Brahmaputra valley's ecosystem."
        ),
        "traditional_technique": (
            "Danced to the dhol (drum), pepa (horn pipe made from buffalo horn), gogona (jaw harp), "
            "and toka (bamboo clapper). Female dancers wear mekhela-chador silk attire; "
            "rapid hip movements, hand gestures, and footwork are characteristic."
        ),
        "why_it_matters": (
            "Rongali Bihu was included in UNESCO's Representative List of Intangible Cultural "
            "Heritage of Humanity in 2023, cementing its global significance."
        ),
        "preservation_status": "thriving",
        "artisan": "Assamese folk dancers and musicians",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/48/Bihu-Dance-assam.jpg",
        "tags": "festival,harvest,Assam,traditional,UNESCO,dhol,pepa,spring",
        "sources": "UNESCO ICH Registry 2023; Assam Tourism; Sangeet Natak Akademi",
        "status": "published",
    },
    {
        "title": "Blue Pottery of Jaipur",
        "slug": "blue-pottery-jaipur",
        "description": (
            "Blue Pottery of Jaipur is a distinctive ceramic art form with Persian–Central Asian "
            "origins. Unusually, it uses no clay: items are made from a dough of quartz stone powder, "
            "glass, Multani mitti (fuller's earth), borax, and gum. The pottery is glazed in "
            "characteristic turquoise-blue and white with floral and geometric patterns."
        ),
        "type": "pottery",
        "region": "Rajasthan",
        "state": "Rajasthan",
        "district": "Jaipur",
        "language": "Rajasthani",
        "community": "Kumbhar artisans of Jaipur",
        "historical_period": "16th century (Mughal period)",
        "cultural_significance": (
            "Blue Pottery was brought to Jaipur by Maharaja Sawai Ram Singh II from Delhi in the "
            "19th century after declining under British rule. The artisan Kripal Singh Shekhawat "
            "is credited with its modern revival in the 1950s and 1960s."
        ),
        "traditional_technique": (
            "The quartz dough is shaped by hand or in plaster moulds, dried, hand-painted with "
            "cobalt oxide (blue) and copper oxide (green) on a white slip glaze, then kiln-fired "
            "at a low temperature of 800°C."
        ),
        "why_it_matters": (
            "GI-tagged. Blue Pottery of Jaipur is an eco-friendly, lead-free craft that represents "
            "a rare synthesis of Persian, Afghan, Mughal, and Rajput traditions."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Kumbhar artisans and Kripal Kumbha workshop, Jaipur",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/af/Dr._Bhau_Daji_Lad_Museum_JEG1715.JPG",
        "tags": "Persian,turquoise,quartz,Jaipur,GI-tag,Mughal,Rajasthan,floral",
        "sources": "Rajasthan Small Industries Corporation; GI Registry",
        "status": "published",
    },
    {
        "title": "Kondapalli Toys",
        "slug": "kondapalli-toys",
        "description": (
            "Kondapalli toys are handcrafted wooden toys from Kondapalli village in Krishna district, "
            "Andhra Pradesh. Made from a soft wood called 'tella poniki', the toys depict mythological "
            "characters, rural life scenes, animals, and market scenes painted in bright, natural colours."
        ),
        "type": "woodwork",
        "region": "South India",
        "state": "Andhra Pradesh",
        "district": "Krishna",
        "language": "Telugu",
        "community": "Aryakshatriya community",
        "historical_period": "400 years",
        "cultural_significance": (
            "Kondapalli toys have been integral to Andhra's Dasara/Navaratri tradition of Bommalattam "
            "(doll arrangement), where elaborate scenes from mythology and daily life are arranged for "
            "worship. The craft has been passed down within the Aryakshatriya community for generations."
        ),
        "traditional_technique": (
            "Tella poniki wood is shaped with a small chisel while wet (it hardens as it dries). "
            "Joints are fixed with sawdust paste. After drying, the toy is coated with chalk "
            "and painted with poster colours in bold, unshaded flat style."
        ),
        "why_it_matters": (
            "GI-tagged. Kondapalli toys are listed as one of the 100 unique products of India and "
            "represent a distinctive strand of South Indian craft culture tied to festival traditions."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Aryakshatriya community artisans, Kondapalli",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/93/Kondapalli_toys_at_a_house_in_Vijayawada.jpg",
        "tags": "soft-wood,bright,mythological,GI-tag,Andhra-Pradesh,Navaratri,Telugu",
        "sources": "AP Handicrafts Development Corporation; GI Registry",
        "status": "published",
    },
    {
        "title": "Theyyam",
        "slug": "theyyam",
        "description": (
            "Theyyam is an ancient ritualistic dance-drama of northern Kerala in which performers "
            "impersonate deities and ancestral spirits. With over 400 distinct forms, each Theyyam "
            "has its own costume, make-up, songs, and ritual procedure. The performer enters a trance "
            "state and is considered to embody the deity."
        ),
        "type": "ritual",
        "region": "North Kerala",
        "state": "Kerala",
        "district": "Kannur",
        "language": "Malayalam / Tulu",
        "community": "Malayan, Vannan, Peruvannan communities",
        "historical_period": "Pre-10th century CE",
        "cultural_significance": (
            "Theyyam inverts the caste hierarchy — the performer, often from a Dalit or lower-caste "
            "community, becomes a deity and must be worshipped by upper-caste members of the community. "
            "It is one of the most socially significant ritual traditions of South Asia."
        ),
        "traditional_technique": (
            "Performers spend hours applying natural make-up (made from rice paste, turmeric, kohl, "
            "and vermillion). Elaborate headgear (mudi) can reach 20 feet in height. Each performance "
            "requires months of preparation and is conducted in sacred groves (kavus) or family shrines."
        ),
        "why_it_matters": (
            "Theyyam preserves one of India's most socially radical spiritual traditions and embodies "
            "over 1,000 years of community memory. No two Theyyam performances are identical."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Theyyam performers of Kannur and Kasaragod",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/38/Kathivanoor_Veeran_Chemmarathi_Thara-Eripuram.jpg",
        "tags": "deity,ritual,costume,oral-tradition,Kerala,Kannur,trance,Dalit",
        "sources": "Kerala Folklore Academy; Sangeet Natak Akademi",
        "status": "published",
    },
    {
        "title": "Yakshagana",
        "slug": "yakshagana",
        "description": (
            "Yakshagana is a traditional theatre form from the coastal districts of Karnataka, "
            "combining dance, music, dialogue, costume, and make-up in all-night performances "
            "based on episodes from the Mahabharata, Ramayana, and Bhagavata Purana. "
            "Performances (called 'melas') travel from village to village during the winter season."
        ),
        "type": "dance",
        "region": "South India",
        "state": "Karnataka",
        "district": "Udupi",
        "language": "Kannada / Tulu",
        "community": "Coastal Karnataka communities",
        "historical_period": "16th century",
        "cultural_significance": (
            "Yakshagana has been the primary medium of religious and moral education for coastal "
            "Karnataka's communities for 500 years. The night-long performances create communal "
            "bonds and transmit epic narratives across generations in living, embodied form."
        ),
        "traditional_technique": (
            "Male actors (Stri Veshas perform female roles) wear elaborate painted make-up "
            "(mukhavarnam) and towering headgear (pagade). Performance combines improvised "
            "dialogue (mattu) with prescribed song (prasanga) set to specific ragas."
        ),
        "why_it_matters": (
            "One of South India's most complete theatrical traditions, integrating all performing "
            "arts. Faces competition from television and cinema but continues to draw large village audiences."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Yakshagana troupes (Melas) of coastal Karnataka",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Yakshaganads.jpg",
        "tags": "theatre,coastal,epic,traditional,Karnataka,Mahabharata,night-performance",
        "sources": "Karnataka Janapada Parishad; Yakshagana Research Centre, Udupi",
        "status": "published",
    },
    {
        "title": "Mising Weaving",
        "slug": "mising-weaving",
        "description": (
            "The Mising tribe of Assam produces intricate handloom textiles on traditional backstrap "
            "looms (mesing ugon looms). Their weaves are known for geometric patterns in vivid colours, "
            "used to create traditional garments including the Mibu Gasor (shawl) and Ugon (wrap skirt). "
            "Every pattern carries meaning within Mising cosmology."
        ),
        "type": "textile",
        "region": "Northeast India",
        "state": "Assam",
        "district": "Dhemaji",
        "language": "Mising",
        "community": "Mising tribe",
        "historical_period": "Pre-historical; documented from 13th century",
        "cultural_significance": (
            "Mising textiles are integral to identity: specific patterns mark age, marital status, "
            "social rank, and clan affiliation. The Mibu Gasor is worn during the Ali Ai Ligang "
            "festival, the most important celebration of the Mising agricultural calendar."
        ),
        "traditional_technique": (
            "Backstrap loom weaving uses the weaver's body as a tension frame. Cotton and silk "
            "threads are dyed with natural colours derived from forest plants. The complex "
            "geometric patterns (called 'miri' or 'teke') are woven from memory."
        ),
        "why_it_matters": (
            "An entirely indigenous textile tradition under threat from cheap synthetic alternatives "
            "and displacement of Mising communities from their traditional forest environments."
        ),
        "preservation_status": "endangered",
        "artisan": "Mising women weavers, Dhemaji and Lakhimpur districts",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/48/DWIJEN_%2843%29.jpg",
        "tags": "tribal,backstrap-loom,geometric,indigenous,Assam,Mising,northeast",
        "sources": "North East Zonal Cultural Centre; Assam Tribal Welfare Department",
        "status": "published",
    },
    {
        "title": "Gond Painting",
        "slug": "gond-painting",
        "description": (
            "Gond painting is a visual art tradition of the Gond tribal people of Madhya Pradesh, "
            "one of India's largest indigenous communities. The paintings, filled with intricate dots "
            "and dashes, depict the Gond world of forests, rivers, animals, and deities in vibrant, "
            "psychedelic colour. Major artist Jangarh Singh Shyam brought this art to world attention."
        ),
        "type": "folk_art",
        "region": "Central India",
        "state": "Madhya Pradesh",
        "district": "Mandla",
        "language": "Gondi",
        "community": "Gond tribe",
        "historical_period": "Ancient; contemporary revival 1980s",
        "cultural_significance": (
            "In Gond tradition, depicting an image of a natural entity — a tree, bird, or river — "
            "honours and strengthens it spiritually. The paintings are therefore simultaneously "
            "artistic, spiritual, and ecological acts within Gond cosmology."
        ),
        "traditional_technique": (
            "Originally painted on walls with earth pigments; now on paper and canvas using acrylic. "
            "Every form is built up from a dense network of lines, dots, and cross-hatching — "
            "no area is left without pattern, echoing the dense forest that is the Gond homeland."
        ),
        "why_it_matters": (
            "Gond painting puts tribal ecological knowledge into visual form and has become an "
            "internationally exhibited contemporary art while remaining rooted in living Gond community practice."
        ),
        "preservation_status": "thriving",
        "artisan": "Gond artists, primarily from Patangarh and Mandla",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/68/JSS_at_BB.jpeg",
        "tags": "tribal,forest,nature,dots,Gondi,Madhya-Pradesh,Jangarh,contemporary",
        "sources": "Bharat Bhavan, Bhopal; Crafts Documentation Project, Indira Gandhi NCSM",
        "status": "published",
    },
    {
        "title": "Cheriyal Scroll Painting",
        "slug": "cheriyal-scroll-painting",
        "description": (
            "Cheriyal scroll painting is a narrative art form from Cheriyal village in Telangana, "
            "practised by the Nakashi community. Using bold red, yellow, blue, and green paints on "
            "cloth scrolls, Nakashi artists depicted stories from the Ramayana, Mahabharata, and "
            "local folk narratives, which itinerant bards used as visual aids during oral performances."
        ),
        "type": "folk_art",
        "region": "South India",
        "state": "Telangana",
        "district": "Siddipet",
        "language": "Telugu",
        "community": "Nakashi community",
        "historical_period": "17th century",
        "cultural_significance": (
            "Cheriyal scrolls served as the 'television' of pre-modern Deccan societies — the Kinnera "
            "bards would unroll scenes while singing the corresponding narrative, making complex "
            "mythological stories accessible to illiterate rural communities."
        ),
        "traditional_technique": (
            "Cotton cloth is treated with rice starch and chalk powder. Bright synthetic and natural "
            "colours are applied in bold flat planes separated by thick black outlines. "
            "Figures are stylised with large eyes, crowns, and ornate jewellery."
        ),
        "why_it_matters": (
            "GI-tagged. Cheriyal painting is at the intersection of visual art and oral performance "
            "tradition — when the bard tradition declines, the painting loses its context and purpose."
        ),
        "preservation_status": "critically_endangered",
        "artisan": "Nakashi community artisans, Cheriyal village",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/75/Cherial_1.jpg",
        "tags": "scroll,narrative,Nakashi,Telangana,GI-tag,bard,visual-storytelling",
        "sources": "Telangana State Handicrafts Corporation; Crafts Council of India",
        "status": "published",
    },
    {
        "title": "Kutiyattam",
        "slug": "kutiyattam",
        "description": (
            "Kutiyattam is the oldest surviving form of Sanskrit theatre, performed in temple theatres "
            "called Kuttampalams attached to major temples in Kerala. A single play — traditionally "
            "performed over 41 nights — allows characters to explore a single couplet's meaning through "
            "elaborate elaboration (nirvahana) spanning entire nights."
        ),
        "type": "ritual",
        "region": "South India",
        "state": "Kerala",
        "district": "Thrissur",
        "language": "Sanskrit / Prakrit / Malayalam",
        "community": "Chakyar and Nangiar communities",
        "historical_period": "10th century CE",
        "cultural_significance": (
            "Kutiyattam is the living vessel of the Sanskrit theatrical tradition codified by "
            "Bharata's Natyashastra. Its elaborate gestural language (mudra) and acting conventions "
            "preserve performance knowledge that would otherwise exist only in manuscripts."
        ),
        "traditional_technique": (
            "Male Chakyar actors and female Nangiar actors undergo lifelong training from childhood. "
            "Elaborate face painting (chutti) takes hours; intricate hand gestures (mudras) have "
            "precise codified meanings. Mizhavu drummers provide rhythmic accompaniment."
        ),
        "why_it_matters": (
            "UNESCO proclaimed Kutiyattam a Masterpiece of the Oral and Intangible Heritage of "
            "Humanity in 2001. It is the only surviving direct link to the 2,000-year-old Sanskrit theatre tradition."
        ),
        "preservation_status": "critically_endangered",
        "artisan": "Chakyar and Nangiar families of Kerala",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/32/Thoranayudham-_Madras1.jpg",
        "tags": "Sanskrit,temple,UNESCO,ancient,Kerala,theatre,mudra,Chakyar",
        "sources": "UNESCO ICH Registry; Kerala Sangeetha Nataka Akademi; Sangeet Natak Akademi",
        "status": "published",
    },
    {
        "title": "Bamboo Craft of Tripura",
        "slug": "bamboo-craft-tripura",
        "description": (
            "The tribal communities of Tripura have for millennia crafted intricate objects from "
            "bamboo — baskets, furniture, fish traps, musical instruments, and architectural elements. "
            "Each of Tripura's 19 tribal communities maintains distinct weaving patterns and uses "
            "that encode their social identity and ecological knowledge."
        ),
        "type": "craft",
        "region": "Northeast India",
        "state": "Tripura",
        "district": "West Tripura",
        "language": "Kokborok",
        "community": "Tripuri, Reang, Jamatia tribes",
        "historical_period": "Pre-historical",
        "cultural_significance": (
            "Bamboo is not merely a material in Tripura's tribal culture — it is a sacred plant "
            "around which cosmological stories, rituals, and life-cycle ceremonies are organised. "
            "The 'Risa' (traditional textile), when made with bamboo-derived thread, marks "
            "clan identity and social status."
        ),
        "traditional_technique": (
            "Bamboo is selected by age and species, sun-dried, split, and scraped into thin "
            "splints using a curved knife (dao). Weaving follows memorised patterns passed "
            "down within families; no written instructions exist. Some tribes smoke-cure "
            "bamboo for durability in humid conditions."
        ),
        "why_it_matters": (
            "Tripura bamboo craft represents an ecosystem-based knowledge system: artisans know "
            "which bamboo species to use for each purpose, conserving biodiversity while "
            "creating sustainable livelihoods in India's second-smallest state."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Tribal artisans of Tripura",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/cd/Woman_weaving_baskets_near_Lake_Ossa.jpg",
        "tags": "bamboo,tribal,weaving,northeast,Tripura,Kokborok,sustainable,indigenous",
        "sources": "Tripura Tribal Areas Autonomous District Council; North East Craft Hub",
        "status": "published",
    },
    {
        "title": "Kalamkari",
        "slug": "kalamkari",
        "description": (
            "Kalamkari ('kalam' = pen, 'kari' = work) is a hand-painted or block-printed cotton "
            "textile art from Andhra Pradesh. The Srikalahasti style uses a pen (kalam) and "
            "natural dyes to create flowing mythological narratives; the Machilipatnam style "
            "uses wooden blocks for geometric and floral prints."
        ),
        "type": "textile",
        "region": "South India",
        "state": "Andhra Pradesh",
        "district": "Chittoor",
        "language": "Telugu",
        "community": "Kalamkari artisan families",
        "historical_period": "3,000 years (documented)",
        "cultural_significance": (
            "Srikalahasti Kalamkari was used to create temple hangings (karuvarai) depicting "
            "Shaivite epics, transforming fabric into portable sacred narrative spaces. "
            "Itinerant artists (chitrakattis) once traveled with armies, painting and singing "
            "narratives of battles and heroes."
        ),
        "traditional_technique": (
            "Cotton cloth undergoes 23 distinct stages including mordanting with myrobalan, "
            "outlining with a bamboo kalam dipped in fermented jaggery and iron solution, "
            "and dyeing with alum-fixed natural colours from indigo, pomegranate rind, and turmeric. "
            "Each colour requires a separate resist-and-dye process."
        ),
        "why_it_matters": (
            "GI-tagged. Kalamkari is a 23-step process that uses only natural materials; "
            "it is one of the world's most environmentally responsible luxury textile traditions."
        ),
        "preservation_status": "vulnerable",
        "artisan": "Kalamkari artisans of Srikalahasti and Machilipatnam",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Kalamkari_painting_of_Lord_Vishnu_on_serpent_Ananta.jpg",
        "tags": "pen,natural-dye,temple,GI-tag,Andhra-Pradesh,block-print,cotton,mythological",
        "sources": "AP Handicrafts Development Corporation; GI Registry",
        "status": "published",
    },
    {
        "title": "Manipuri Raas Leela",
        "slug": "manipuri-raas-leela",
        "description": (
            "Manipuri Raas Leela is a classical dance-drama form from Manipur depicting episodes "
            "from the life of Krishna, performed in an all-night ceremony during the full moon of "
            "the Hindu month of Kartik. It is one of India's eight classical dance forms, "
            "characterised by lyrical, circular movements and luminous white costumes."
        ),
        "type": "dance",
        "region": "Northeast India",
        "state": "Manipur",
        "district": "Imphal West",
        "language": "Meitei (Manipuri)",
        "community": "Meitei Vaishnava community",
        "historical_period": "18th century (Maharaja Bhagyachandra's era)",
        "cultural_significance": (
            "Manipuri Raas Leela was revealed to Maharaja Bhagyachandra in a divine dream in 1779 "
            "and has been performed continuously since. It synthesises indigenous Meitei movement "
            "aesthetics with the devotional Vaishnavism that transformed Manipuri society."
        ),
        "traditional_technique": (
            "Female dancers (Radha and the Gopis) wear a stiffened barrel-shaped skirt (potloi) "
            "with intricate gold embroidery. Movement is in a constant slow revolution, "
            "arms tracing circular arcs. No footwork is audible — the dance is 'silent'."
        ),
        "why_it_matters": (
            "Recognised as one of India's classical dance traditions by the Sangeet Natak Akademi. "
            "Manipuri Raas Leela shaped the trajectory of modern Indian dance through "
            "Rabindranath Tagore's encounter with it in 1919."
        ),
        "preservation_status": "thriving",
        "artisan": "Manipuri dancers trained in the Gurumayum, Senaton, and Atombapu gharanas",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Jagoi_Manipuri_dance_1.jpg",
        "tags": "classical,Krishna,dance,Manipuri,Vaishnavism,circular,potloi,northeast",
        "sources": "Sangeet Natak Akademi; Jawaharlal Nehru Manipur Dance Academy",
        "status": "published",
    },
]


def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        existing = db.query(HeritageItem).count()
        if existing > 0:
            print(f"[seed] Database already has {existing} items. Skipping seed.")
            print("[seed] To re-seed, delete 'katha_kosh.db' and run again.")
            return

        print(f"[seed] Inserting {len(ITEMS)} heritage items...")
        for i, item_data in enumerate(ITEMS):
            item = HeritageItem(**item_data)
            db.add(item)
            if (i + 1) % 10 == 0:
                db.flush()
                print(f"[seed]   {i + 1} items inserted...")

        # Create default admin user
        admin_exists = db.query(User).filter(User.username == "admin").first()
        if not admin_exists:
            admin = User(
                username="admin",
                email="admin@kathakosh.in",
                hashed_password=hash_password("KathaKosh@2024"),
                role="admin",
                full_name="Kathā-Kosh Administrator",
                is_active=True,
            )
            db.add(admin)
            print("[seed] Created admin user (username: admin, password: KathaKosh@2024)")

        db.commit()
        print(f"[seed] ✅ Successfully seeded {len(ITEMS)} heritage items.")
        print("[seed] Admin credentials — username: admin | password: KathaKosh@2024")

        # Optionally index all items in vector store
        try:
            from app.services.search_service import search_service
            items = db.query(HeritageItem).all()
            print(f"[seed] Indexing {len(items)} items in vector store...")
            for item in items:
                try:
                    search_service.index_item(item)
                except Exception as e:
                    print(f"[seed]   Vector index failed for '{item.title}': {e}")
            print("[seed] Vector indexing complete.")
        except Exception as e:
            print(f"[seed] Vector indexing skipped: {e}")

    except Exception as e:
        db.rollback()
        print(f"[seed] ❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
