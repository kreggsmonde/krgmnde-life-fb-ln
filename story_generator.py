import os, sys, json, time, requests, re
import config

RELATIONSHIP_CURRICULUM = [
    [
        "Les Secrets de l'Attachement Émotionnel",
        "Comprendre nos styles d'attachement, nos peurs profondes et comment aimer en toute sécurité"
    ],
    [
        "L'Art de Communiquer sans Blesser",
        "Exprimer ses besoins avec tendresse et clarté, sans tomber dans le reproche ou la défense"
    ],
    [
        "Apprendre à Poser des Limites Saines",
        "Savoir dire non avec bienveillance pour préserver l'harmonie du couple et son estime de soi"
    ],
    [
        "Guérir de la Peur du Rejet et de l'Abandon",
        "Retrouver sa sécurité intérieure et construire une confiance inébranlable dans le lien"
    ],
    [
        "Les 5 Langages de l'Amour au Quotidien",
        "Décoder les besoins affectifs profonds de votre partenaire pour nourrir l'amour chaque jour"
    ],
    [
        "La Vulnérabilité : Force Invisible du Couple",
        "Pourquoi oser se montrer authentique et imparfait est la seule véritable clé de l'intimité"
    ],
    [
        "Désamorcer les Conflits sans Rancœur",
        "Transformer les désaccords en opportunités de rapprochement et de compréhension mutuelle"
    ],
    [
        "Sortir de la Dépendance Affective",
        "Comment cultiver son autonomie émotionnelle et s'épanouir pleinement à deux"
    ],
    [
        "L'Écoute Active et le Pouvoir du Silence",
        "Entendre ce que le cœur de l'autre murmure derrière la fatigue et les mots du quotidien"
    ],
    [
        "Reconstruire la Confiance Après une Blessure",
        "Le chemin patient de la réparation, de la vérité et du pardon partagé"
    ]
]

DEFAULT_5_ACTS = [
    ("Acte 1 : Le Constat du Cœur", "Introduction chaleureuse et immersion dans la réalité du défi relationnel"),
    ("Acte 2 : Les Racines Inconscientes", "Exploration psychologique des peurs, des blessures d'enfance et de nos réflexes de défense"),
    ("Acte 3 : Clés Pratiques & Paroles d'Apaisement", "Phrases transformatrices, attitudes bienveillantes et dialogues constructifs au quotidien"),
    ("Acte 4 : Traverser les Tempêtes Émotionnelles", "Gérer la colère, le repli sur soi et surmonter les moments de tension sans panique"),
    ("Acte 5 : L'Exercice du Cœur & Bénédiction Quotidienne", "Défi d'introspection bienveillant, rituel de connexion pour la semaine et message d'espoir")
]

def load_history_topics() -> list:
    """Reads all past published topics from published_videos.json and history.json to ensure no repeats."""
    past = []
    for fname in ["published_videos.json", "history.json"]:
        fpath = os.path.join(config.BASE_DIR, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get("topic"):
                                t = item["topic"].strip()
                                if t not in past:
                                    past.append(t)
            except Exception:
                pass
    return past

def generate_dynamic_topic_ai(past_topics: list, ep_num: int = 1) -> dict:
    """Queries Pollinations AI with past topics history to generate a brand new non-repeating French relationship topic."""
    key = config.POLLINATIONS_API_KEY
    if not key:
        return None

    past_sample = past_topics[-30:] if len(past_topics) > 30 else past_topics
    prompt = (
        f"Tu es la productrice exécutive et conceptrice du podcast français '{config.CHANNEL_NAME}'.\n"
        f"Slogan : {config.TAGLINE}\n"
        f"Format : Podcast solo intime animé par {config.HOST1_NAME}, une psychologue et confidente bienveillante.\n"
        f"Thématique : Les relations humaines, la psychologie amoureuse, l'attachement, la communication, la tendresse, la résilience du couple.\n"
        f"Consigne linguistique : TOUT doit être rédigé en français élégant, naturel et chaleureux.\n\n"
        f"Épisodes déjà traités (NE PAS RÉPÉTER) :\n"
        + json.dumps(past_sample, indent=2, ensure_ascii=False) + "\n\n"
        f"Génère UN NOUVEAU sujet d'épisode captivant et profondément enrichissant pour l'Épisode #{ep_num}.\n\n"
        f"FORMAT DE SORTIE : Renvoie UNIQUEMENT un objet JSON valide (aucun markdown extérieur, pas de préambule) :\n"
        "{\n"
        f'  "id": "ep_{ep_num}",\n'
        '  "topic": "Titre captivant en français (ex: Apprendre à Pardonner sans s\'Oublier)",\n'
        '  "focus": "Aperçu en une phrase de ce que l\'auditeur va comprendre et transformer dans ses liens affectifs",\n'
        '  "thumbnail_title_1": "PREMIERS MOTS (MAX 16 CARACTÈRES)",\n'
        '  "thumbnail_title_2": "DEUXIÈMES MOTS (MAX 16 CARACTÈRES)",\n'
        '  "thumbnail_hook": "Accroche percutante (ex: Sauver son Couple en Douceur)",\n'
        '  "acts": [\n'
        '    ["Acte 1 : Titre", "Description du focus de l\'acte..."],\n'
        '    ["Acte 2 : Titre", "Description du focus de l\'acte..."],\n'
        '    ["Acte 3 : Titre", "Description du focus de l\'acte..."],\n'
        '    ["Acte 4 : Titre", "Description du focus de l\'acte..."],\n'
        '    ["Acte 5 : Titre", "Description du focus de l\'acte..."]\n'
        '  ]\n'
        "}"
    )

    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": config.POLLINATIONS_MODEL,
        "messages": [
            {"role": "system", "content": "Tu es un producteur de podcast haut de gamme. Tu réponds exclusivement en JSON valide."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.82
    }

    for attempt in range(3):
        try:
            print(f"[StoryGenerator] Synthèse IA d'un nouveau sujet relationnel (tentative {attempt+1}/3)...")
            resp = requests.post(config.POLLINATIONS_ENDPOINT, json=payload, headers=headers, timeout=25)
            if resp.status_code == 200:
                raw = resp.json()["choices"][0]["message"]["content"].strip()
                if "```" in raw:
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:].strip()
                    raw = raw.split("```")[0].strip()
                data = json.loads(raw)
                topic_val = data.get("topic", "")
                if topic_val and data.get("acts") and len(data["acts"]) >= 4:
                    t_lower = topic_val.lower().strip()
                    past_lowers = [p.lower().strip() for p in past_topics]
                    if t_lower not in past_lowers:
                        print(f"[StoryGenerator] Nouveau sujet généré avec succès : '{topic_val}'")
                        return data
        except Exception as e:
            print(f"[StoryGenerator] Erreur tentative sujet IA ({attempt+1}) : {e}")
            time.sleep(1.5)
    return None

def get_next_topic(history: list, custom_topic: str = None, ep_num: int = 1) -> dict:
    if custom_topic:
        words = custom_topic.split()
        mid = len(words) // 2
        t1 = " ".join(words[:mid]) if mid > 0 else words[0]
        t2 = " ".join(words[mid:]) if mid > 0 else "RELATIONS"
        return {
            "id": f"custom_{ep_num}",
            "topic": custom_topic,
            "focus": "Une réflexion intime et apaisante sur la dynamique des relations humaines",
            "thumbnail_title_1": t1[:16].upper(),
            "thumbnail_title_2": t2[:16].upper(),
            "thumbnail_hook": "Comprendre le Cœur",
            "acts": DEFAULT_5_ACTS
        }

    past_topics = load_history_topics()

    # 1. AI Dynamic Generation
    ai_topic = generate_dynamic_topic_ai(past_topics, ep_num=ep_num)
    if ai_topic:
        t1 = ai_topic.get("thumbnail_title_1", "")
        t2 = ai_topic.get("thumbnail_title_2", "")
        if not t1 or not t2:
            words = ai_topic["topic"].split()
            mid = len(words) // 2
            t1 = " ".join(words[:mid])
            t2 = " ".join(words[mid:])
        return {
            "id": ai_topic.get("id", f"ep_{ep_num}"),
            "topic": ai_topic["topic"],
            "focus": ai_topic.get("focus", "Comprendre et nourrir nos relations affectives"),
            "thumbnail_title_1": t1[:16].upper(),
            "thumbnail_title_2": t2[:16].upper(),
            "thumbnail_hook": ai_topic.get("thumbnail_hook", "Psychologie du Couple"),
            "acts": ai_topic.get("acts", DEFAULT_5_ACTS)
        }

    # 2. Curated Curriculum Fallback
    past_lowers = [p.lower().strip() for p in past_topics]
    for idx, (title, focus) in enumerate(RELATIONSHIP_CURRICULUM):
        if title.lower().strip() not in past_lowers:
            print(f"[StoryGenerator] Sujet du catalogue sélectionné : '{title}'")
            words = title.split()
            mid = len(words) // 2
            t1 = " ".join(words[:mid])
            t2 = " ".join(words[mid:])
            return {
                "id": f"ep_{ep_num}",
                "topic": title,
                "focus": focus,
                "thumbnail_title_1": t1[:16].upper(),
                "thumbnail_title_2": t2[:16].upper(),
                "thumbnail_hook": "L'Art du Lien Humain",
                "acts": DEFAULT_5_ACTS
            }

    # 3. Endless Cycle Variation
    cycle = (ep_num - 1) // len(RELATIONSHIP_CURRICULUM) + 1
    cat_idx = (ep_num - 1) % len(RELATIONSHIP_CURRICULUM)
    base_title, base_focus = RELATIONSHIP_CURRICULUM[cat_idx]
    title = f"{base_title} : Approfondissement & Guérison (Partie {cycle})"
    words = title.split()
    mid = len(words) // 2
    t1 = " ".join(words[:mid])
    t2 = " ".join(words[mid:])
    return {
        "id": f"ep_{ep_num}",
        "topic": title,
        "focus": f"Approfondissement essentiel : {base_focus}",
        "thumbnail_title_1": t1[:16].upper(),
        "thumbnail_title_2": t2[:16].upper(),
        "thumbnail_hook": f"Approche Thérapeutique #{cycle}",
        "acts": DEFAULT_5_ACTS
    }

def generate_curated_fallback_act(act_idx: int, act_title: str, topic: str, target_turns: int = 40) -> list:
    """Master French relationship monologue turns written with therapeutic warmth and poetic elegance."""
    h1 = config.HOST1_NAME
    s1 = config.HOST1_SPEAKER
    cname = config.CHANNEL_NAME

    solo_act_scripts = [
        # Acte 1 : Le Constat du Cœur
        [
            f"Bienvenue dans {cname}. Je suis heureuse de vous retrouver aujourd'hui pour ce moment d'intimité.",
            f"Aujourd'hui, nous prenons le temps de nous arrêter sur un sujet essentiel : {topic}.",
            "Dans le tumulte de nos vies quotidiennes, nous oublions souvent d'écouter les battements de notre cœur.",
            "Les relations humaines sont à la fois notre plus grand refuge et notre plus grand miroir.",
            "Lorsque nous aimons, nous mettons à nu nos désirs les plus profonds, mais aussi nos fragilités.",
            "Vous avez peut-être ressenti cette incompréhension silencieuse qui s'installe parfois entre deux êtres.",
            "Deux personnes qui s'aiment profondément, mais qui ne parviennent plus à se comprendre.",
            "Prenez une profonde respiration avec moi, et déposez toutes les tensions accumulées.",
            "Ce podcast est votre sanctuaire, un espace où la vulnérabilité devient une immense force.",
            "Nous ne sommes pas ici pour chercher la perfection ou distribuer des reproches.",
            "Nous sommes ici pour comprendre la danse complexe et délicate de deux âmes qui tentent de se lier.",
            "Regardez les personnes qui comptent le plus pour vous dans votre vie.",
            "Combien de fois avez-vous retenu un mot d'amour par pudeur ou par crainte du rejet ?",
            "L'amour ne souffre pas de trop de présence, mais de la peur de ne pas être accueilli.",
            "Ensemble, nous allons éclairer ces zones d'ombre avec bienveillance et tendresse.",
            "Laissez ces paroles résonner doucement en vous au fil de notre écoute.",
            "Chaque relation est un chef-d'œuvre vivant, constamment en train de se réinventer.",
            "Et le premier pas vers l'autre commence toujours par un regard apaisé sur soi-même.",
            "Installez-vous confortablement, nous avançons pas à pas vers cette belle découverte."
        ],
        # Acte 2 : Les Racines Inconscientes
        [
            "Pour comprendre ce qui se joue dans nos relations d'aujourd'hui, il faut souvent regarder en arrière.",
            "Nos manières d'aimer et de nous attacher prennent racine dans nos toutes premières expériences d'enfance.",
            "Ce sont nos premiers liens familiaux qui ont façonné notre boussole émotionnelle.",
            "Si nous avons manqué de sécurité affective, nous pouvons développer une peur panique de l'abandon.",
            "À l'inverse, si nous nous sommes sentis étouffés, l'engagement peut ressembler à une prison dorée.",
            "Ces réflexes inconscients, ce sont nos styles d'attachement, nos armures protectrices.",
            "Lorsque notre partenaire s'éloigne pour respirer, notre enfant intérieur peut paniquer et crier.",
            "Nous croyons alors que l'amour disparaît, alors qu'il s'agit simplement d'un besoin d'espace.",
            "Comprendre cela change absolument tout dans la dynamique d'un couple.",
            "Vous ne combattez plus contre l'autre, vous comprenez enfin les peurs cachées derrière ses réactions.",
            "La colère n'est souvent qu'un appel désespéré à être vu, reconnu et rassuré.",
            "Lorsque nous voyons la fragilité derrière le masque de l'indifférence ou du reproche, la tendresse renaît.",
            "C'est là que commence la véritable guérison : cesser de juger, et commencer à ressentir.",
            "Accueillez ces souvenirs avec douceur, car ils ont fait de vous la personne sensible que vous êtes aujourd'hui.",
            "Vous avez le pouvoir d'écrire un nouveau chapitre relationnel, empreint de sécurité et de paix."
        ],
        # Acte 3 : Clés Pratiques & Paroles d'Apaisement
        [
            "Entrons maintenant dans la pratique quotidienne de cette communication du cœur.",
            "Le plus grand piège dans un échange est d'attaquer l'identité de l'autre plutôt que d'exprimer son ressenti.",
            "Remplacer le fameux 'Tu ne fais jamais attention à moi' par un simple 'Je me sens seul en ce moment'.",
            "Voyez comme cette simple nuance désamorce instantanément le besoin de contre-attaque.",
            "Quand vous parlez de vous, avec franchise et vulnérabilité, vous invitez l'autre à vous consoler.",
            "Quand vous accusez, vous le forcez à revêtir son armure et à se justifier.",
            "Un autre secret merveilleux réside dans l'art des petites attentions imprévues.",
            "Un regard chaleureux au milieu de la pièce, un mot doux laissé sur la table, une étreinte prolongée.",
            "Ces gestes minuscules envoient à notre système nerveux un signal puissant : tu es en sécurité avec moi.",
            "N'attendez pas les grands anniversaires pour célébrer la présence de la personne aimée.",
            "C'est la régularité des petits signes d'amour qui tisse le fil invisible de la confiance.",
            "Et lorsque l'autre vous parle, essayez d'écouter sans chercher immédiatement à résoudre le problème.",
            "La plupart du temps, l'être humain n'attend pas de solution magique, il veut simplement être entendu.",
            "Dire simplement 'Je te comprends, et je suis là avec toi' a un pouvoir de guérison infini.",
            "Faites l'expérience aujourd'hui : offrez une écoute totale et sans jugement à quelqu'un que vous aimez."
        ],
        # Acte 4 : Traverser les Tempêtes Émotionnelles
        [
            "Même avec la plus grande sagesse, les tempêtes et les frictions font partie intégrante de la vie à deux.",
            "Deux êtres qui partagent leur quotidien auront inévitablement des moments de désaccord et de fatigue.",
            "Le secret d'un couple durable ne réside pas dans l'absence de conflit, mais dans la façon dont on le traverse.",
            "Lorsque la tension monte et que le ton s'élève, notre cerveau entre en mode de survie.",
            "Dans cet état d'alerte, aucune conversation constructive ne peut aboutir.",
            "Le geste le plus courageux consiste alors à proposer une pause apaisante : 'Je t'aime, mais prenons dix minutes pour respirer'.",
            "Ce temps de recul permet au cœur de ralentir et d'éviter les mots blessants que l'on regrette.",
            "La fierté et l'ego sont les pires conseillers quand il s'agit d'amour.",
            "Demandez-vous toujours : préférez-vous avoir raison à tout prix, ou préférez-vous être en paix et en lien ?",
            "Reconnaître ses propres torts n'est jamais un aveu de faiblesse, c'est le sommet de l'élégance du cœur.",
            "Un pardon sincère lave les cicatrices et fortifie le lien bien au-delà de son état d'origine.",
            "Traverser l'orage main dans la main crée une complicité inestimable que rien ne peut ébranler.",
            "Ayez confiance dans la force de votre amour face aux turbulences passagères."
        ],
        # Acte 5 : L'Exercice du Cœur & Bénédiction Quotidienne
        [
            "Nous voici arrivés au terme de cette belle réflexion partagée sur notre chaîne.",
            "Pour ancrer cette prise de conscience dans votre vie, voici le défi du cœur que je vous propose cette semaine.",
            "Ce soir ou demain, prenez un instant pour dire à une personne chère ce que sa présence vous apporte de beau.",
            "Ne parlez pas de ce qu'elle fait, mais de ce qu'elle est pour vous, de la lumière qu'elle diffuse.",
            "Vous verrez à quel point un mot sincère peut illuminer un visage et réchauffer une journée entière.",
            "Rappelez-vous que vous méritez d'être aimé avec respect, douceur et considération.",
            "Et commencez par vous offrir à vous-même cette même bienveillance chaque matin devant le miroir.",
            f"Je vous remercie infiniment pour votre écoute et votre fidélité sur {cname}.",
            "Pensez à vous abonner pour ne manquer aucun de nos rendez-vous doux et éclairants.",
            "Prenez grand soin de vous, de vos proches, et cultivez toujours l'art précieux du lien humain.",
            "À très bientôt pour un nouvel épisode plein de tendresse et de clarté."
        ]
    ]

    safe_act_idx = min(act_idx, len(solo_act_scripts) - 1)
    lines = solo_act_scripts[safe_act_idx]
    result = []
    for l in lines:
        result.append({"speaker": s1, "name": h1, "text": l})
        if len(result) >= target_turns:
            break

    while len(result) < target_turns:
        for l in lines:
            prefix = "En y réfléchissant avec le cœur, "
            result.append({"speaker": s1, "name": h1, "text": f"{prefix}{l[0].lower() + l[1:] if len(l) > 1 else l}"})
            if len(result) >= target_turns:
                break

    return result

def generate_act_ai(act_idx: int, act_title: str, topic_title: str, focus: str, target_turns: int = 35) -> list:
    key = config.POLLINATIONS_API_KEY
    if not key:
        return None

    if act_idx == 0:
        transition_note = "Acte d'ouverture : Accueille chaleureusement l'auditeur sur la chaîne, installe une atmosphère douce, intime et introduit le thème avec sensibilité."
    elif act_idx == 1:
        transition_note = "Acte 2 : IMPORTANT - Ne dis PAS 'bienvenue' ou 'bienvenue à nouveau'. Enchaîne directement et naturellement avec les racines psychologiques et l'inconscient."
    elif act_idx == 2:
        transition_note = "Acte 3 : IMPORTANT - Ne dis PAS 'bienvenue'. Enchaîne avec fluidité sur les exemples concrets du quotidien, la communication douce et les paroles d'apaisement."
    elif act_idx == 3:
        transition_note = "Acte 4 : IMPORTANT - Ne dis PAS 'bienvenue'. Poursuis avec la gestion des crises, des disputes et la guérison des blessures sans panique."
    else:
        transition_note = "Acte 5 (Clôture) : IMPORTANT - Transition douce vers l'exercice pratique de la semaine, un message d'espoir pour le couple et le mot de conclusion chaleureux."

    prompt = (
        f"Tu rédiges le script d'un épisode de podcast intime et réconfortant pour la chaîne '{config.CHANNEL_NAME}'.\n"
        f"Animatrice unique : {config.HOST1_NAME} (psychologue et spécialiste des relations humaines, voix féminine chaleureuse, empathique et bienveillante).\n"
        f"Format : MONOLOGUE SOLO en français où elle s'adresse directement à l'auditeur ('vous') comme à un ami cher ou en consultation intime.\n"
        f"Thématique de l'épisode : {topic_title}\n"
        f"Section actuelle : {act_title}\n"
        f"Focus émotionnel : {focus}\n"
        f"Consigne de transition : {transition_note}\n\n"
        f"EXIGENCES STRICTES :\n"
        f"- Exactement {target_turns} répliques de monologue successives prononcées par {config.HOST1_NAME}.\n"
        f"- Chaque réplique doit faire entre 14 et 24 mots, avec un style parlé naturel, fluide, touchant et élégant.\n"
        f"- Vocabulaire psychologique accessible, empreint de bienveillance, de nuances et de sagesse émotionnelle.\n"
        f"- Renvoie UNIQUEMENT un tableau JSON brut d'objets (pas de markdown, pas de texte d'accompagnement) :\n"
        f"[\n"
        f'  {{"speaker": "{config.HOST1_SPEAKER}", "name": "{config.HOST1_NAME}", "text": "..."}},\n'
        f'  {{"speaker": "{config.HOST1_SPEAKER}", "name": "{config.HOST1_NAME}", "text": "..."}}\n'
        f"]"
    )

    try:
        resp = requests.post(
            config.POLLINATIONS_ENDPOINT,
            json={
                "model": config.POLLINATIONS_MODEL,
                "messages": [
                    {"role": "system", "content": "Tu es un générateur d'émissions de radio et podcasts haut de gamme. Tu réponds exclusivement en JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.78
            },
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            timeout=25
        )
        if resp.status_code == 200:
            raw = resp.json()["choices"][0]["message"]["content"].strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:].strip()
                raw = raw.split("```")[0].strip()
            parsed = json.loads(raw)
            min_needed = max(2, min(target_turns, 8))
            if isinstance(parsed, list) and len(parsed) >= min_needed:
                result_turns = []
                for p in parsed:
                    txt = p.get("text", "").strip()
                    if not txt:
                        continue
                    result_turns.append({"speaker": config.HOST1_SPEAKER, "name": config.HOST1_NAME, "text": txt})

                # Sanitize repetitive greetings in Acts 2-5
                if act_idx > 0 and result_turns:
                    first_text = result_turns[0]["text"]
                    for prefix in ["bienvenue", "bonjour et bienvenue", "bienvenue à nouveau", "bonjour à tous"]:
                        if first_text.lower().startswith(prefix):
                            cleaned = re.sub(r"^(?:bienvenue(?:\s+à\s+nouveau)?(?:\s+dans\s+[^.!?]*)?[.!?]\s*|bonjour\s+(?:et\s+bienvenue\s+)?[^.!?]*[.!?]\s*)", "", first_text, flags=re.IGNORECASE).strip()
                            if cleaned:
                                result_turns[0]["text"] = cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned
                            else:
                                result_turns[0]["text"] = f"Poursuivons notre réflexion sur {topic_title} en nous penchant sur nos comportements au quotidien."
                            break

                if len(result_turns) >= target_turns:
                    return result_turns[:target_turns]
                elif len(result_turns) >= min_needed:
                    fallback_turns = generate_curated_fallback_act(act_idx, act_title, topic_title, target_turns=target_turns)
                    seen_texts = set(r["text"] for r in result_turns)
                    for ft in fallback_turns:
                        if len(result_turns) >= target_turns:
                            break
                        if ft["text"] not in seen_texts:
                            result_turns.append(ft)
                            seen_texts.add(ft["text"])
                    return result_turns[:target_turns]
    except Exception as e:
        print(f"  [AI Note] Acte {act_idx+1} retourné en script curé de secours : {e}")
    return None

def generate_full_podcast_story(target_minutes: float = 20.0, topic: str = None, ep_num: int = 1) -> dict:
    history = load_history_topics()
    topic_info = get_next_topic(history, custom_topic=topic, ep_num=ep_num)
    selected_topic = topic_info["topic"]
    acts_meta = topic_info.get("acts", DEFAULT_5_ACTS)

    print(f"[StoryGenerator] Épisode #{ep_num} - Thématique : '{selected_topic}'")

    # Target 20 minutes calibrated with slower -6% speech rate and 0.75s natural pauses (~6.5s per turn)
    turns_per_act = int(max(4, (target_minutes * 60) / (len(acts_meta) * 6.5)))
    if target_minutes <= 1.0:
        turns_per_act = 4
    elif target_minutes <= 3.0:
        turns_per_act = 8

    dialogue = []
    chapters = []

    for act_idx, (act_title, act_focus) in enumerate(acts_meta):
        chapters.append({"title": act_title, "start_turn": len(dialogue)})
        print(f"  [Acte {act_idx+1}/5] Génération de '{act_title}' ({turns_per_act} répliques)...")

        turns = generate_act_ai(act_idx, act_title, selected_topic, act_focus, target_turns=turns_per_act)
        if not turns:
            turns = generate_curated_fallback_act(act_idx, act_title, selected_topic, target_turns=turns_per_act)

        dialogue.extend(turns)

    print(f"[StoryGenerator] Monologue complet généré : {len(dialogue)} répliques réparties sur {len(acts_meta)} actes.")
    return {
        "topic": selected_topic,
        "thumbnail_title_1": topic_info["thumbnail_title_1"],
        "thumbnail_title_2": topic_info["thumbnail_title_2"],
        "thumbnail_hook": topic_info["thumbnail_hook"],
        "chapters": chapters,
        "dialogue": dialogue
    }

def generate_metadata(topic: str, duration_sec: float, chapters: list, ep_num: int = 1) -> dict:
    title = f"{topic} | {config.CHANNEL_NAME} Ép. {ep_num}"
    lines = [
        f"🎙️ Bienvenue dans {config.CHANNEL_NAME} avec {config.HOST1_NAME} - Épisode #{ep_num} !",
        f"Thème du jour : {topic}",
        "",
        "🕒 CHAPITRES & HORODATAGES :"
    ]
    for ch in chapters:
        m = int(ch.get("start_time", 0) // 60)
        s = int(ch.get("start_time", 0) % 60)
        lines.append(f"{m:02d}:{s:02d} - {ch['title']}")

    lines.extend([
        "",
        "💡 Un voyage doux et éclairant au cœur de la psychologie des relations humaines, de l'amour et de l'intimité émotionnelle.",
        "👉 Abonnez-vous pour recevoir chaque semaine un nouvel épisode apaisant et inspirant.",
        f"#{config.CHANNEL_NAME.replace(' ', '').replace('\'', '')} #Psychologie #RelationsHumaines #AmourEtCouple #PodcastFrancais #DeveloppementPersonnel #Attachement"
    ])

    return {
        "title": title[:100],
        "description": "\n".join(lines),
        "tags": ["relations humaines", "psychologie couple", "podcast francais", "amour", "communication bienveillante", "attachement emotionnel", config.CHANNEL_NAME.lower()]
    }
